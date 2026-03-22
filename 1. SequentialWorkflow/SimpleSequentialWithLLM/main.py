from langgraph.graph import StateGraph, START, END
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.2-1B-Instruct",
    task="text-generation",
)

model = ChatHuggingFace(llm=llm)

class LLMState(TypedDict):
    question : str
    response : str

def llm_answer(state : LLMState) -> LLMState:
    question = state['question']

    prompt = f'Answer the following question {question} with the least no. of words possible that is as short as possible'

    response = model.invoke(prompt).content

    state['response'] = response

    return state

graph = StateGraph(LLMState)

#create nodes
graph.add_node('llm_answer', llm_answer)

#create edges

graph.add_edge(START, 'llm_answer')
graph.add_edge('llm_answer', END)

workflow = graph.compile()

question = input("Ask the question or the query: ")

initial_state = { 'question': question}
final_state = workflow.invoke(initial_state)

print(final_state['response'])


graph_image = workflow.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_image)

response = final_state['response']
with open("Sample_result.txt", "a") as f:
    f.write(f"Question : {question}\n")
    f.write(f"Answer: {response}\n")
