from fastapi import APIRouter, HTTPException, Depends
from database import UserRepository as ur, QuestionRepository as questr, QuizesRepository as qr
from schemas import *

default_router = APIRouter()

users_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

quizes_router = APIRouter(
    prefix="/quizes",
    tags=["Квизы"]
)

questions_router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"]
)


@users_router.get('')
async def users_get() -> list[User]:
    return await ur.get_users()


@users_router.get('/u2')
async def users_get2() -> dict[str, list[User] | str]:
    users = await ur.get_users()
    return {'status': 'ok', 'data': users}


@users_router.get('/{id}')
async def user_get(id: int) -> User:
    user = await ur.get_user(id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@users_router.post('')
async def add_user(user: UserAdd = Depends()) -> UserId:
    id = await ur.add_user(user)
    return {'id': id}

# ---------------------------------------Quizes


@quizes_router.get('')
async def quizes_get() -> dict[str, list[Quize] | str]:
    quizes = await qr.get_quizes()
    return {'status': 'ok', 'data': quizes}


@quizes_router.post('')
async def add_quize(quize: QuizeAdd = Depends()) -> QuizeId:
    id = await qr.add_quize(quize)
    return {'id': id}


@quizes_router.get('/{id}')
async def quize_get(id: int) -> Quize:
    quize = await qr.get_quize(id)
    if quize:
        return quize
    raise HTTPException(status_code=404, detail="Quize not found")


# @quizes_router.get('/{id}/questions1')
# async def quiz_questions_get(id: int) -> Quize:
#     quize = await qr.get_quiz_questions(id)
#     if quize:
#         return quize
#     raise HTTPException(status_code=404, detail="Quize not found")


# ---------------------------------------Questions


@questions_router.get('')
async def questions_get() -> dict[str, list[Question] | str]:
    question = await questr.get_questions()
    return {'status': 'ok', 'data': question}


@questions_router.post('')
async def add_question(question: QuestionAdd = Depends()) -> QuestionId:
    id = await questr.add_question(question)
    return {'id': id}


@questions_router.get('/{id}')
async def question_get(id: int) -> Question:
    question = await questr.get_question(id)
    if question:
        return question
    raise HTTPException(status_code=404, detail="Quize not found")
