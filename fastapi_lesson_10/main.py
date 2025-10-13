from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from routers import default_router, users_router, quizes_router, questions_router
from database import DataRepository as dr


@asynccontextmanager  # реагирует на  методы __aenter__() и __aexit__()
async def lifespan(app: FastAPI):
    await dr.create_table()
    print("-------База создана-------")
    await dr.add_user_data()
    await dr.add_question_data()
    await dr.add_quize_data()
    print("-------База построена-------")

    yield
    await dr.delete_table()
    print("-------База очищена-------")


app = FastAPI(lifespan=lifespan)

app.include_router(default_router)
app.include_router(users_router)
app.include_router(quizes_router)
app.include_router(questions_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
