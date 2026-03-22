from langgraph.graph import StateGraph, START, END
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.2-1B-Instruct",
    task="text-generation",
)

model = ChatHuggingFace(llm = llm)

class BlogState(TypedDict):
    title : str
    outline : str
    content : str


def create_outline(state:BlogState) -> BlogState:

    title = state['title']

    prompt = f"""
    Generate a clear and well-structured blog outline (maximum 100 words) for the topic: "{title}".

Requirements:
- Include a short introduction section.
- Provide 4 to 6 main sections with descriptive headings.
- End with a conclusion section.
- Design the outline in such a way that the blog content can be completed with in 300 words.

Formatting:
- Use clear headings.
- Strictly do not use any type of symbols or anything like that.
- Keep the outline concise and easy to understand.
- Ensure logical flow from introduction to conclusion.
- Do not mention anything about word limits in the output.

The outline should be informative, organized, and suitable for writing a blog post.


"""

    outline = model.invoke(prompt).content
    
    state['outline'] = outline
    
    return state

def create_blog(state:BlogState) -> BlogState:

    title = state['title']
    outline = state['outline']
    
    prompt = f"""
    Write a well-structured blog post on the topic: {title}.

Follow the outline strictly:
{outline}

Requirements:
- Start with a clear and engaging introduction.
- Expand each point in the outline with short sentences.
- Use simple, clear, and professional language.
- Try to complete the whole discussion in less than 400 words strictly.
- End with a concise conclusion.

Formatting:
- Use headings and subheadings where appropriate.
- Do not include any type of symbols.
- Avoid repetition and unnecessary filler content.

Output should be clean, well-organized, and easy to read."""
    
    content = model.invoke(prompt).content
    
    state['content'] = content

    return state


graph = StateGraph(BlogState)

#add nodes
graph.add_node('create_outline', create_outline)
graph.add_node('create_blog', create_blog)

#add edges
graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_blog')
graph.add_edge('create_blog', END)

workflow = graph.compile()
title = input("What is the blog topic: ")
initial_state = {'title': title}

final_state = workflow.invoke(initial_state)

print("Title : ")
print(final_state['title'],"\n")
print(final_state['outline'],"\n")
print("Here is the blog content,\n")
print(final_state['content'])

with open("SampleResponses.txt", "a") as f:
    f.write("="*35 + "New Sample" + "="*35 + "\n\n")
    f.write(f"Title : {final_state['title']}\n\n")
    f.write(f"Outline : \n {final_state['outline']}\n\n")
    f.write(f"Blog content:\n\n {final_state['content']}\n\n")

graph_image = workflow.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as g:
    g.write(graph_image)


