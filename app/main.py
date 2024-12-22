import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Any

from fastapi import FastAPI

from consumers.notification_consumer import consume


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Асинхронный контекстный менеджер, управляющий жизненным циклом приложения.

    Создаёт задачу для потребления уведомлений при запуске приложения
    и корректно завершает её при остановке.

    :param app: Экземпляр FastAPI.
    :type app: FastAPI
    :return: None
    :rtype: AsyncIterator[None]
    """
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
@app.get("/")
async def health_check() -> dict[str, Any]:
    """
    Возвращает простой JSON-ответ со статусом работы приложения.

    :return: Словарь со статусом.
    :rtype: dict[str, Any]
    """
    return {"status": "ok"}
