from langgraph.graph import StateGraph,START, END
from models import TweetState
from functions import (
    evaluate_tweet,
    generate_tweet,
    optimize_tweet,
    route_evaluation
)

graph = StateGraph(TweetState)

graph.add_node('generate', generate_tweet)
graph.add_node('evaluate', evaluate_tweet)
graph.add_node('optimize', optimize_tweet)

graph.add_edge(START, 'generate')
graph.add_edge('generate', 'evaluate')
graph.add_conditional_edges('evaluate', route_evaluation, {'approved' : END, 'needs_improvement':'optimize'})
graph.add_edge('optimize', 'evaluate')

workflow = graph.compile()

graph_image = workflow.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as g:
    g.write(graph_image)

topic = input("Enter the topic: ")
initial_state = {
    "topic": topic,
    "iteration": 1,
    "max_iteration": 5
}
result = workflow.invoke(initial_state)

with open("sample_output.txt", "a") as t:
    t.write("="*30 + " New sample " + "="*30 + "\n\n")
    t.write(f"Topic : {result['topic']}\n")
    for tweet in result['tweet_history']:
        t.write(f"Tweet : {tweet}\n\n")

