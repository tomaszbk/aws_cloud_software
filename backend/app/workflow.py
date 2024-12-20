from typing import Annotated, TypedDict

from fastapi.routing import APIRouter
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode

from app.config import cfg
from app.database.dynamo_get import get_product_details, get_products
from app.database.dynamo_insert import add_purchase, insert_user
from app.database.models import Category, OrchestrationAction, Product, User
from app.send_event import send_event_to_eventbridge

router = APIRouter()

if cfg.DEBUG == "False":
    from langchain_aws import ChatBedrockConverse

    llm = ChatBedrockConverse(
        model=cfg.AWS_BEDROCK_MODEL,
        region_name=cfg.AWS_BEDROCK_REGION,
    )
else:
    from langchain_ollama.chat_models import ChatOllama

    llm = ChatOllama(model="llama3.2-vision", base_url="http://aws-ollama:11434")


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    latest_user_prompt: str


def merge_tools(messages: list):
    print("merge_tools called")
    for index, message in enumerate(messages):
        if type(message) is AIMessage and type(message.content[0]) is dict:
            if message.content[0]["type"] == "tool_use":
                tool_use_message = messages.pop(index)
                tool_name = tool_use_message.content[0]["name"]
                next_message = messages[index]
                if type(next_message) is ToolMessage:
                    tool_message = messages.pop(index)
                    messages.insert(
                        index,
                        AIMessage(
                            "The "
                            + tool_name
                            + " tool was called and the result was "
                            + tool_message.content
                        ),
                    )
    return messages


# TOOLS
def choose_action(action: OrchestrationAction):
    """Chooses the action to use based on the chat history.
    NORMAL_CONVERSATION : if the user asks about the business, what we offer, what categories of products we have, who we are, or none of below.
    GET_PRODUCTS : if the user specifies the category of products he wants to see, or wants to get details of a product.
    PURCHASE : if the user wants to purchase a product, or is in the middle of a purchase process."""
    return action


def get_product_details_tool(product_id: str) -> Product:
    """Returns details of the product with the specified id."""
    return get_product_details(product_id)


def route_agent(state: State):
    action = state["messages"][-1].content
    match action:
        case "NORMAL_CONVERSATION":
            return "conversation_agent"
        case "GET_PRODUCTS":
            return "products_agent"
        case "PURCHASE":
            return "purchase_agent"
        case _:
            return "conversation_agent"
    return action


def make_purchase(
    product_id: str, product_category: Category, user_name: str, user_email: str, user_phone_number
) -> str:
    """Makes a purchase for the specified product and user.
    The user data must be provided as a dictionary, NOT a string."""
    user = User(name=user_name, email=user_email, phone_number=user_phone_number)
    insert_user(user)
    product: Product = get_product_details(product_id, product_category)
    purchase_result = add_purchase(user.phone_number, product)

    print(purchase_result)
    send_event_to_eventbridge(user_email, user_name, product.image_url)
    return purchase_result


def get_user_data(user_language: str) -> str:
    """Requests the user to provide their name, email and phone number.
    Requires the user's language: es or en."""
    match user_language:
        case "es":
            return "Por favor, proporciona tu nombre, email y número de teléfono."
        case "en":
            return "Please provide your name, email and phone number."
        case _:
            return f"(Debug: opcion no valida: {user_language})Please provide your name, email and phone number."


orchestration_tools = [choose_action]
orchestration_tool_node = ToolNode(orchestration_tools)
orchestration_model = llm.bind_tools(orchestration_tools)

conversation_model = llm

products_tools = [get_products]
products_tools_node = ToolNode(products_tools)
products_model = llm.bind_tools(products_tools)

purchase_tools = [make_purchase, get_user_data]
purchase_tools_node = ToolNode(purchase_tools)
purchase_model = llm.bind_tools(purchase_tools)


# Define the function that determines whether to continue or not
def should_continue_products_agent(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "products_tools"
    return END


# Define the function that calls the model
def call_orchestrator_agent(state: State):
    prompt = """You're an orchestor agent that will call the choose_action tool
    to determine the agent to call next.
    Use the tool, dont answer directly.
    Read the chat history to determine the action to take.
    To know which categories we offer, use the conversational agent
    """
    messages = merge_tools(state["messages"].copy())
    latest_user_prompt = messages[-1].content
    messages.append(SystemMessage(content=prompt))
    response = orchestration_model.invoke(messages)

    return {"messages": [response], "latest_user_prompt": latest_user_prompt}


def call_conversation_agent(state: State):
    prompt = """Your name is utn-bot. You are a helpful assistant that solves user questions about this ecommerce.
            The ecommerce is called utn-shop. We sell these categories: tv, cellphone, laptop.
            We are open everyday from 9am to 5pm. We are located at 1234 Main St, Anytown, USA.
            Our payment methods are credit card, paypal, bitcoin and mercado pago."""
    messages = merge_tools(state["messages"].copy())
    messages.append(SystemMessage(content=prompt))
    messages.append(HumanMessage(state["latest_user_prompt"]))
    response = conversation_model.invoke(messages)
    return {"messages": [response]}


def call_products_agent(state: State):
    prompt = """You're an agent that can access the products database.
    We have the following categories of products: tv, cellphone, laptop.
    Do not offer products that were not returned from a tool call.
    """
    messages = state["messages"]
    messages = merge_tools(messages.copy())
    messages.append(SystemMessage(content=prompt))
    messages.append(HumanMessage(state["latest_user_prompt"]))
    response = products_model.invoke(messages)
    return {"messages": [response]}


def call_purchase_agent(state: State):
    prompt = """You're an agent that will handle the purchase of a product.
    If the user hasn't provided his name and email, ask for it.
    """
    messages = merge_tools(state["messages"].copy())
    messages.append(SystemMessage(content=prompt))
    messages.append(HumanMessage(state["latest_user_prompt"]))
    response = purchase_model.invoke(messages)
    return {"messages": [response]}


def should_retry_purchase_agent(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "purchase_tools"
    return "purchase_agent"


workflow = StateGraph(State)

workflow.add_node("orchestration_agent", call_orchestrator_agent)
workflow.add_node("conversation_agent", call_conversation_agent)
workflow.add_node("orchestration_tools", orchestration_tool_node)

workflow.add_node("products_agent", call_products_agent)
workflow.add_node("products_tools", products_tools_node)

workflow.add_node("purchase_agent", call_purchase_agent)
workflow.add_node("purchase_tools", purchase_tools_node)

workflow.add_edge(START, "orchestration_agent")
workflow.add_edge("orchestration_agent", "orchestration_tools")

workflow.add_edge("products_tools", "conversation_agent")

workflow.add_conditional_edges(
    "orchestration_tools",
    route_agent,
)
workflow.add_conditional_edges(
    "products_agent",
    should_continue_products_agent,
)

workflow.add_conditional_edges(
    "purchase_agent",
    should_retry_purchase_agent,
)

workflow.add_edge("conversation_agent", END)
workflow.add_edge("products_agent", END)

# workflow.add_edge("purchase_agent", "purchase_tools")
workflow.add_edge("purchase_tools", END)


# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

app = workflow.compile(checkpointer=checkpointer)


@router.post("/user-message")
async def handle_user_message(user_prompt: str, thread_id: str):
    final_state = app.invoke(
        {"messages": [HumanMessage(content=user_prompt)]},
        config={"configurable": {"thread_id": thread_id}},
    )

    return final_state["messages"][-1].content
