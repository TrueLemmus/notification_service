import asyncio

from fastapi import FastAPI
from consumers.notification_consumer import consume


app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    asyncio.run(consume())
