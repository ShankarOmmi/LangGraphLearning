
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_community.tools import DuckDuckGoSearchRun
from models import ChatState

load_dotenv()

llm = ChatGoogleGenerativeAI(model ='gemini-2.5-flash')

raw_search = DuckDuckGoSearchRun(region = "us-en")

@tool
def search(query: str):
    """Search the web using DuckDuckGo"""
    result = raw_search.run(query)

    # Normalize only DuckDuckGo output
    if isinstance(result, list) and len(result) > 0:
        if isinstance(result[0], dict) and "text" in result[0]:
            return result[0]["text"]

    return result

@tool
def calculator(first_num:float, second_num:float, operation : str):
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

tools = [search, calculator]

llm_with_tools = llm.bind_tools(tools)

def chat_node(state:ChatState):
    """LLM node that may answer or request a tool call"""
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages":response}

tool_node = ToolNode(tools)

