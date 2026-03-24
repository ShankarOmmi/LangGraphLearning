from langgraph.graph import StateGraph, START, END
from models import ChatState
from langchain_core.messages import BaseMessage, HumanMessage
from functions import chat_node



graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile()

graph_image = chatbot.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as g:
    g.write(graph_image)



question = input("Ask your question: ")

prompt = f"""
        Answer the following question {question} as short as possible"""


initial_state = { 'messages' : [HumanMessage(content = prompt)]}

response = chatbot.invoke(initial_state)['messages'][-1].content

print(response)

with open("sample_outputs.txt", "a") as t :
    t.write("="*20+"New Sample"+"="*20+"\n")
    t.write(f'User : {question}\n')
    t.write(f'ChatBot : {response}\n\n')