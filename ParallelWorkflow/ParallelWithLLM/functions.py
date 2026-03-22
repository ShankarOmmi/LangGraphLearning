from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from models import EvaluationSchema, PasswordState

load_dotenv()

model = ChatGoogleGenerativeAI(model ='gemini-2.5-flash')

structured_model = model.with_structured_output(EvaluationSchema)

def feedback_length(state: PasswordState) -> PasswordState:
    password = state['password']
    length = len(password)

    if length < 6:
        feedback = "Very weak length"
        score = 2
    elif 6 <= length < 8:
        feedback = "Weak length"
        score = 4
    elif 8 <= length < 12:
        feedback = "Good length"
        score = 7
    elif 12 <= length <= 16:
        feedback = "Strong length"
        score = 9
    else:
        feedback = "Too long (not practical)"
        score = 6

    return {
        'length_fb': feedback,
        'individual_scores': [{'length_score':score}]
    }

def feedback_diversity(state: PasswordState) -> PasswordState:
    password = state['password']

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    types_count = sum([has_lower, has_upper, has_digit, has_special])

    if types_count == 4:
        feedback = "Excellent character diversity"
        score = 10
    elif types_count == 3:
        feedback = "Good diversity but can be improved"
        score = 8
    elif types_count == 2:
        feedback = "Limited diversity"
        score = 5
    else:
        feedback = "Very poor diversity"
        score = 2

    return {
        'diversity_fb': feedback,
        'individual_scores': [{'diversity_score': score}]
    }

def feedback_patterns(state:PasswordState) -> PasswordState:

    password = state['password']

    prompt = f"""
    You are a cybersecurity expert.

    Evaluate the following password based on the presence of predictable patterns:

    Password: {password}

    Check for:
    - sequential patterns (e.g., 1234, abcd)
    - repeated characters (e.g., aaa, 111)
    - common words or phrases (e.g., "password", "admin")
    - keyboard patterns (e.g., qwerty, asdf)

    Instructions:
    - If the password contains obvious patterns → lower score
    - If the password is random and unpredictable → higher score

    Return:
    - A short, clear feedback explaining any patterns found (or absence of them)
    - A score out of 10 (integer)

    Keep the response concise and focused only on pattern strength.
    """
    output = structured_model.invoke(prompt)

    return {'pattern_fb' : output.feedback,
            'individual_scores': [{'pattern_score': output.score}]}

def feedback_strength(state: PasswordState) -> PasswordState:

    prompt = f"""
    Create a concise overall password strength feedback.

    Length feedback: {state['length_fb']}
    Diversity feedback: {state['diversity_fb']}
    Pattern feedback: {state['pattern_fb']}

    Explain clearly and briefly.
    """

    output = model.invoke(prompt)
    scores_dict = {}
    for item in state['individual_scores']:
        scores_dict.update(item)
    avg_score = round(sum(scores_dict.values()) / len(scores_dict),2)

    return {
        'strength_fb': output.content,
        'avg_score': avg_score
    }
