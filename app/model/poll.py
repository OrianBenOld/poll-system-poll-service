from typing import Optional
from pydantic import BaseModel


class PollQuestionBase(BaseModel):
    title: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str


class PollQuestionCreate(PollQuestionBase):
    pass


class PollQuestionUpdate(BaseModel):
    title: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None


class PollQuestion(PollQuestionBase):
    id: int


class AnswerCreate(BaseModel):
    user_id: int
    option_choice: str


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    user_id: int
    option_choice: str
