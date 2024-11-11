from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    chosen_answer: str
