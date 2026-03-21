from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MarksState(TypedDict):
    math_marks : float
    science_marks : float
    average : float
    result : str

def calculate_average(state : MarksState) -> MarksState:
    math_marks = state['math_marks']
    science_marks = state['science_marks']

    average = (math_marks + science_marks)//2

    state['average'] = round(average, 2)

    return state

def result(state : MarksState) -> MarksState:
    average = state['average']

    if average < 35:
        state["result"] = "Fail"
    elif 35<=average<55:
        state["result"] = "Second Class"
    elif 55<=average<75 :
        state["result"] = "First Class"
    else:
        state["result"] = "Distinction"
    
    return state

graph = StateGraph(MarksState)

#add nodes to the graph
graph.add_node('calculate_average', calculate_average)
graph.add_node('result', result)

#add edges to your graph

graph.add_edge(START, 'calculate_average')
graph.add_edge('calculate_average', 'result')
graph.add_edge('result', END)

#compile the graph
workflow = graph.compile()

math_marks, science_marks = map(float,input("Enter math marks and science marks one by one (seperated by a comma):").split(','))
initial_state= { 'math_marks':math_marks, 'science_marks': science_marks}

final_state = workflow.invoke(initial_state)
print(final_state)


# from IPython.display import Image
image = workflow.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(image)