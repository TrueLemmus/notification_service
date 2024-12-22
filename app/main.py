import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from consumers.notification_consumer import consume


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Старт приложения: запускаем асинхронную задачу
    task = asyncio.create_task(consume())

    # Передаём управление дальше (обычный yield)
    yield

    # Завершение приложения: отменяем задачу и ждём
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)


@app.get("/health")
@app.get('/')
async def health_check():
    return {"status": "ok"}


# if __name__ == "__main__":
#     asyncio.run(consume())
