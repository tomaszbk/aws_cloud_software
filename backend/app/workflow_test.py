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

def merge_tools(messages: list ):
    for index, message in enumerate(messages):
        if type(message) is AIMessage and message.content[0]['type'] == 'tool_use':
            print("tool_use found")
            tool_use_message = messages.pop(index)
            tool_name = tool_use_message.content[0]['name']
            next_message = messages[index]
            if type(next_message) is ToolMessage:
                print("tool_message found")
                tool_message = messages.pop(index)
                messages.insert(index, AIMessage("The " + tool_name + " tool was called and the result was " + tool_message.content))
    return messages
    

graph_builder = StateGraph(State)

def call_chatbot_agent(state: State):
    prompt = """You're an  agent that will call the numbers_tool tool.
    Use the tool, dont answer directly.
    Read the chat history to determine the numbers.
    """
    print("chatbot_agent called")
    messages = merge_tools(state["messages"].copy())
    #messages = state["messages"].copy()
    return {"messages": [chat_model.invoke(messages)]}

def numbers():
    """Prints numbers."""
    print("numbers tool called")
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

print("user: gimme numbers")
stream_graph_updates("gimme numbers")
print("user: again")
stream_graph_updates("again")
print("user: again2")
stream_graph_updates("again")
print("user: again3")
stream_graph_updates("again")
print("user: again")
stream_graph_updates("again")
print("user: again2")



