
from langgraph.graph import StateGraph, START, END
from models import PasswordState
from functions import (
    feedback_length,
    feedback_diversity,
    feedback_patterns,
    feedback_strength)      



#create graph
graph = StateGraph(PasswordState)

#add nodes

graph.add_node('fb_length', feedback_length)
graph.add_node('fb_diversity', feedback_diversity)
graph.add_node('fb_pattern', feedback_patterns)
graph.add_node('fb_strength', feedback_strength)

#create edges
graph.add_edge(START, 'fb_length')
graph.add_edge(START, 'fb_diversity')
graph.add_edge(START, 'fb_pattern')

graph.add_edge('fb_length', 'fb_strength')
graph.add_edge('fb_diversity', 'fb_strength')
graph.add_edge('fb_pattern', 'fb_strength')

graph.add_edge('fb_strength', END)

workflow = graph.compile()

graph_image = workflow.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as g:
    g.write(graph_image)

password = input("Enter your password: ")
initial_state = {'password' : password}

evaluation = workflow.invoke(initial_state)
label = ""
if evaluation['avg_score'] < 3:
    label = "Very Weak"
elif 3 <= evaluation['avg_score'] < 5:
    label = "Weak"
elif 5 <= evaluation['avg_score'] < 7:
    label = "Medium"
else:
    label = "Strong"

scores_dict = {}
for item in evaluation['individual_scores']:
    scores_dict.update(item)

with open("sample_output.txt", "a") as t:
    t.write("="*30 + " New sample " + "="*30 + "\n\n")
    t.write(f"Password : {evaluation['password']}\n")
    t.write(f"Length Feedback : {evaluation['length_fb']}\n")
    t.write(f"Length Score : {scores_dict['length_score']}\n")
    t.write(f"Diversity Feedback : {evaluation['diversity_fb']}\n")
    t.write(f"Diversity Score : {scores_dict['diversity_score']}\n")
    t.write(f"Patterns Feedback : {evaluation['pattern_fb']}\n")
    t.write(f"Pattern Score : {scores_dict['pattern_score']}\n")
    t.write(f"Overall Feedback : {evaluation['strength_fb']}\n")
    t.write(f"Overall Score : {evaluation['avg_score']}\n")
    t.write(f"Strength of the password : {label}\n\n")

