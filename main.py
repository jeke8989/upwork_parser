import asyncio

from loguru import logger
from core import get_single_job, start_subscription
import json
from fastapi import FastAPI
from api.api_v1 import endpoints
import uvicorn

app = FastAPI(title="UpworkAPI")

app.include_router(endpoints.router)

if __name__ == "__main__":
    logger.add("logs/log_{time}.log", level="DEBUG", rotation="5 day")
    
    # Запуск асинхронной функции перед запуском сервера
    asyncio.run(start_subscription())
    uvicorn.run(app, host="0.0.0.0", port=7618)

