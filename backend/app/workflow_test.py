from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from langchain_aws import ChatBedrockConverse


llm = ChatBedrockConverse(
        model="us.meta.llama3-2-11b-instruct-v1:0",
        region_name="us-west-2",
        credentials_profile_name="tz"
    )
        
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


graph_builder = StateGraph(State)

def call_chatbot_agent(state: State):
    prompt = """You're an  agent that will call the numbers_tool tool
    if it hasnt been called yet.
    Use the tool, dont answer directly, otherwise end.
    Read the chat history to determine the action to take.
    """
    return {"messages": [chat_model.invoke(state["messages"])]}

def numbers():
    """Prints numbers."""
    print("example")
    return "123456"



numbers_tools = [numbers]
numbers_tool_node = ToolNode(numbers_tools)
chat_model = llm.bind_tools(numbers_tools)


graph_builder.add_node("chatbot_agent", call_chatbot_agent)

graph_builder.add_node("numbers_tools", numbers_tool_node)

graph_builder.add_edge("chatbot_agent", "numbers_tools")

graph_builder.add_edge(START, "chatbot_agent")

graph_builder.add_edge("chatbot_agent", END)

checkpointer = MemorySaver()

app = graph_builder.compile(checkpointer=checkpointer)


def stream_graph_updates(user_input: str):
    for event in app.stream({"messages": [("user", user_input)]},
                            config={"configurable": {"thread_id": 1}}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)



while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break