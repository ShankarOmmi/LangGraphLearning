from typing import TypedDict, Literal
from pydantic import BaseModel, Field

class SentimentSchema(BaseModel):
    sentiment : Literal["positive", "negative"] = Field(description = 'Sentiment of the review')

class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(description='The category of issue mentioned in the review')
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description='The emotional tone expressed by the user')
    urgency: Literal["low", "medium", "high"] = Field(description='How urgent or critical the issue appears to be')

class ReviewState(TypedDict):

    review : str
    sentiment : Literal["positive", "negative"]
    diagnosis : str
    response : str