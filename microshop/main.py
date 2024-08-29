from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api_v1 import router as router_v1
from core.config import settings
from items_views import router as items_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Когда мы используем alembic мы больше не выполняем
    # автоматическое создание таблиц.
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    yield
    # Код для очистки может быть добавлен здесь, если это необходимо


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {"message": "Hello brothers!"}


@app.get("/hello")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!!!"}


@app.get("/calc/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
