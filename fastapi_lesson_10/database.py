from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select
from models import UserOrm, Model, QuestionOrm, QuizeOrm
from schemas import *
import os

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, 'fastapi_lesson_10.db')

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)

    @classmethod
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)

    @classmethod
    async def add_user_data(cls):
        async with new_session() as session:
            users = [
                UserOrm(name='Хельга', age=33, phone='331122'),
                UserOrm(name='Андрей', age=34, phone='1122334455'),
                UserOrm(name='Кира', age=4),
                UserOrm(name='Денис', age=5),
                UserOrm(name='Ника', age=33, phone='111'),
                UserOrm(name='Дима', age=33)
            ]

            session.add_all(users)
            await session.flush()
            await session.commit()

    @classmethod
    async def add_question_data(cls):
        async with new_session() as session:
            questions = [
                QuestionOrm(question='Сколько будет 2+2*2?', answer='6', wrong1='4', wrong2='8', wrong3='10'),
                QuestionOrm(question='Сколько месяцев в году имеют 28 дней?', answer='Все', wrong1='Один', wrong2='Ни одного', wrong3='Два'),
                QuestionOrm(question='Каким станет зелёный утёс, если упадет в Красное море?', answer='Мокрым', wrong1='Красным', wrong2='Не изменится', wrong3='Фиолетовым'),
                QuestionOrm(question='Какой рукой лучше размешивать чай?', answer='Ложкой', wrong1='Правой', wrong2='Левой', wrong3='Любой'),
                QuestionOrm(question='Что не имеет длины, глубины, ширины, высоты, а можно измерить?', answer='Время', wrong1='Глупость', wrong2='Море', wrong3='Воздух'),
                QuestionOrm(question='Когда сетью можно вытянуть воду?', answer='Когда вода замерзла', wrong1='Воздушный шар', wrong2='Парашют', wrong3='Облако'),
                QuestionOrm(question='Что такое у меня в кармашке?', answer='Кольцо', wrong1='Кулак', wrong2='Дырка', wrong3='Бублик')
            ]

            session.add_all(questions)
            await session.flush()
            await session.commit()


    @classmethod
    async def add_quize_data(cls):
        async with new_session() as session:
            quizes = [
                QuizeOrm(name_quize='КВИЗ1', id_question1=5, id_question2=4, id_question3=8)
                , QuizeOrm(name_quize='КВИ2', id_question1=7, id_question2=3, id_question3=5)
                , QuizeOrm(name_quize='КВИЗ3', id_question1=4, id_question2=5, id_question3=2)
                , QuizeOrm(name_quize='КВИЗ4', id_question1=6, id_question2=3, id_question3=1)
                , QuizeOrm(name_quize='КВИЗ5', id_question1=7, id_question2=2, id_question3=5)
            ]

            session.add_all(quizes)
            await session.flush()
            await session.commit()

class UserRepository:

    @classmethod
    async def add_user(cls, user: UserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump()
            user = UserOrm(**data)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_users(cls) -> list[UserOrm]:
        async with new_session() as session:
            query = select(UserOrm)

            res = await session.execute(query)
            users = res.scalars().all()  # -> список
            return users

    @classmethod
    async def get_user(cls, id) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == id)
            res = await session.execute(query)
            user = res.scalars().first()
            return user


class QuestionRepository:

    @classmethod
    async def add_question(cls, question: QuestionAdd) -> int:
        async with new_session() as session:
            data = question.model_dump()
            question = QuestionOrm(**data)
            session.add(question)
            await session.flush()
            await session.commit()
            return question.id

    @classmethod
    async def get_questions(cls) -> list[QuestionOrm]:
        async with new_session() as session:
            query = select(QuestionOrm)

            res = await session.execute(query)
            questions = res.scalars().all()  # -> список
            return questions

    @classmethod
    async def get_question(cls, id) -> QuestionOrm:
        async with new_session() as session:
            query = select(QuestionOrm).where(QuestionOrm.id == id)
            res = await session.execute(query)
            question = res.scalars().first()
            return question


class QuizesRepository:

    @classmethod
    async def add_quize(cls, quize: QuizeAdd) -> int:
        async with new_session() as session:
            data = quize.model_dump()
            quize = QuizeOrm(**data)
            session.add(quize)
            await session.flush()
            await session.commit()
            return quize.id

    @classmethod
    async def get_quizes(cls) -> list[QuizeOrm]:
        async with new_session() as session:
            query = select(QuizeOrm)
            res = await session.execute(query)
            quizes = res.scalars().all()
            return quizes

    @classmethod
    async def get_quize(cls, id) -> QuizeOrm:
        async with new_session() as session:
            query = select(QuizeOrm).where(QuizeOrm.id == id)
            res = await session.execute(query)
            quize = res.scalars().first()
            return quize

    @classmethod
    async def get_quiz_questions(cls, id) -> (int, ):
        async with new_session() as session:
            query = select(QuizeOrm).where(QuizeOrm.id == id)
            print(query)
            res = await session.execute(query)
            quize = res.scalars().first()
            return (quize.id_question1, quize.question1.question)
