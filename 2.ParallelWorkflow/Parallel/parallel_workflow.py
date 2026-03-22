from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class TextState(TypedDict):
    text : str

    word_count : int
    char_count : int
    summary : str

def word_count(state:TextState)-> TextState:

    text = state['text']

    word_count = len(text.split())

    # state['word_count'] = word_count If updated like this 
    # we need to return whole state and if we do so then that
    # will result in error in parallel workflows, 
    # so instead return only the updated value only

    return {'word_count': word_count} #returning only the updated value

def char_count(state:TextState)-> TextState:

    text = state['text']

    char_count = len(text)

    return {'char_count': char_count}

def summary(state:TextState)->TextState:
    
    word_count = state['word_count']
    char_count = state['char_count']
    summary = f""" The text consists of 
    {word_count} words with 
    {char_count} characters"""

    
    return {'summary' : summary}

#Create Graph
graph = StateGraph(TextState)

#add nodes
graph.add_node('calculate_words', word_count)
graph.add_node('calculate_characters', char_count)
graph.add_node('summarise', summary)

#add edges
graph.add_edge(START, 'calculate_words')
graph.add_edge(START, 'calculate_characters')
graph.add_edge('calculate_words', 'summarise')
graph.add_edge('calculate_characters','summarise')
graph.add_edge('summarise', END)

workflow = graph.compile()

graph_image = workflow.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as g:
    g.write(graph_image)

text = input("Enter your text")
initial_state = {'text': text}

response_dict = workflow.invoke(initial_state)

with open("sampleOutputs.txt", "a") as t:
    t.write("="*30 + "New Output" + "="*30 + "\n")
    t.write(f"Given text : {response_dict['text']}\n")
    t.write(f"No. of words : {response_dict['word_count']}\n")
    t.write(f"No. of characters : {response_dict['char_count']}\n\n")




