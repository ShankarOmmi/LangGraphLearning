from langgraph.graph import StateGraph, START, END
from models import ChatState
from langchain_core.messages import BaseMessage, HumanMessage
from functions import (
    tools,
    chat_node,
    tool_node
)
from langgraph.prebuilt import tools_condition


graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, 'chat_node')
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

workflow = graph.compile()

graph_image = workflow.get_graph().draw_mermaid_png()
with open ("graph.png", "wb") as g:
    g.write(graph_image)

message = input("Enter your question : ")
out = workflow.invoke({"messages": [HumanMessage(content= message)]})

result = out["messages"][-1].content

with open("sample_output.txt", "a") as t:
    t.write(f"Human: {message}\n")
    t.write(f"Bot: {result}\n")

