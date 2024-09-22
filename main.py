import asyncio

from loguru import logger
from core import get_single_job, start_subscription
import json
from fastapi import FastAPI
from api.api_v1 import endpoints
import uvicorn

async def lifespan(app: FastAPI):
    #logger.add("py_log.log", level="DEBUG", rotation="5 day")
    
    # Запуск асинхронной функции при старте приложения
    await start_subscription()
    
    yield  # Это указывает на окончание фазы старта

app = FastAPI(title="UpworkAPI", lifespan=lifespan)

app.include_router(endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7618)