
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
import operator


class EvaluationSchema(BaseModel):

    feedback : str = Field(description = 'Detailed Feedback for the password')
    score : int = Field(description = 'Score out of 10', ge=0, le =10)


class PasswordState(TypedDict):

    password : str

    length_fb : str
    diversity_fb : str
    pattern_fb : str
    strength_fb : str

    individual_scores: Annotated[list[dict], operator.add]
    avg_score : float
