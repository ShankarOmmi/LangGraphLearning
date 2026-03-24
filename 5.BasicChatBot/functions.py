
from langchain_google_genai import ChatGoogleGenerativeAI
from models import ChatState
from dotenv import load_dotenv



load_dotenv()

llm = ChatGoogleGenerativeAI(model ='gemini-2.5-flash')

def chat_node(state:ChatState):

    messages = state['messages']

    response = llm.invoke(messages)

    return {'messages':[response]}