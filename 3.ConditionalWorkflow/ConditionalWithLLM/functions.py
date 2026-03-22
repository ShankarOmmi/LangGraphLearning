from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import Literal
from model import SentimentSchema, DiagnosisSchema
from model import ReviewState

load_dotenv()

model = ChatGoogleGenerativeAI(model ='gemini-2.5-flash')

structured_model1 = model.with_structured_output(SentimentSchema)
structured_model2 = model.with_structured_output(DiagnosisSchema)

def find_sentiment(state: ReviewState) -> ReviewState:
    prompt = f"For the following review find out the sentiment \n {state['review']}"
    sentiment = structured_model1.invoke(prompt).sentiment

    return {'sentiment': sentiment}

def check_sentiment(state : ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    if state['sentiment'] == 'positive':
        return 'positive_response'
    else :
        return 'run_diagnosis'

def positive_response(state : ReviewState):

    prompt = f""" write a warm thank you response message in this review:
    \n\n"{state['review']}" \n
    Also, kindly ask the user to leave the feedback"""

    response = model.invoke(prompt).content

    return {'response' : response}

def run_diagnosis(state: ReviewState) -> ReviewState:

    prompt = f""" Diagnose this negative review; \n\n{state['review']}\n 
    Return the issue_type, tone and urgency"""

    response = structured_model2.invoke(prompt)

    return {'diagnosis': response.model_dump()}

def negative_response(state: ReviewState) -> ReviewState:

    diagnosis = state['diagnosis']

    prompt = f"""You are a support assistant.
    The user had a '{diagnosis['issue_type']}' issue,
    sounded '{diagnosis['tone']}', and marked urgency as 
    '{diagnosis['urgency']}'.
    Write an empathetic, helpful resolution message in less than 200 words
    """

    response = model.invoke(prompt).content

    return {'response': response}



