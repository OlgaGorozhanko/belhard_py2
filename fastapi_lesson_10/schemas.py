from pydantic import BaseModel, ConfigDict


# USER ----------------

class UserAdd(BaseModel):
    name: str
    age: int
    phone: str | None = None


class User(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserId(BaseModel):
    id: int


# Question ----------------

class QuestionAdd(BaseModel):
    question: str
    answer: str
    wrong1: str
    wrong2: str
    wrong3: str


class Question(QuestionAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class QuestionId(BaseModel):
    id: int


# Quize ----------------

class QuizeAdd(BaseModel):
    name_quize: str
    id_question1: int
    id_question2: int
    id_question3: int


class Quize(QuizeAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class QuizeId(BaseModel):
    id: int
