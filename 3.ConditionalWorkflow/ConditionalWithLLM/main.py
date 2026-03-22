from langgraph.graph import StateGraph, START, END
from model import ReviewState
from functions import (
    find_sentiment,
    positive_response,
    run_diagnosis,
    negative_response,
    check_sentiment
    )


graph = StateGraph(ReviewState)

graph.add_node('find_sentiment', find_sentiment)
graph.add_node('positive_response', positive_response)
graph.add_node('run_diagnosis', run_diagnosis)
graph.add_node('negative_response', negative_response)

#add edges

graph.add_edge(START,'find_sentiment')
graph.add_conditional_edges('find_sentiment', check_sentiment)
graph.add_edge('positive_response', END)
graph.add_edge('run_diagnosis', 'negative_response')
graph.add_edge('negative_response', END)

workflow = graph.compile()

graph_image = workflow.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as g:
    g.write(graph_image)

review = input (" Enter your review: ")

initial_state = {'review' : review, 'diagnosis' : None}
final_state = workflow.invoke(initial_state)

with open("sample_output.txt", "a") as t:
    t.write("="*30 + " New sample " + "="*30 + "\n\n")
    t.write(f"Review : {final_state['review']}\n")
    t.write(f"Sentiment : {final_state['sentiment']}\n")
    t.write(f"Diagnosis: {final_state['diagnosis']}\n")
    t.write(f"Response : {final_state['response']}\n\n")



