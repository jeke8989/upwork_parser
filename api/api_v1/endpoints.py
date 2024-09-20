import traceback
from fastapi import APIRouter
from core import get_info_list, get_single_job, event_job_subscription
from loguru import logger as logging
import asyncio

logging.add("py_log.log", level="DEBUG")
router = APIRouter()

@router.get('/list_jobs')
async def get_list_jobs_upwork(url: str):
    try:
        return await get_info_list(url=url)
    except Exception as e:
        logging.exception(e)
        msg = f"error: {e.__class__.__name__}. message: {e}. traceback: {traceback.format_exc()}"
        return {"ok": False, "message": msg}
        
    
@router.get('/job')
async def get_job_upwork(url: str):
    try:
        return await get_single_job(url=url)
    except Exception as e:
        logging.exception(e)
        msg = f"error: {e.__class__.__name__}. message: {e}. traceback: {traceback.format_exc()}"
        return {"ok": False, "message": msg}
    

@router.get('/set_subscription')
async def get_list_jobs_upwork(url: str, api_key: str):
    try:
        return await get_info_list(url=url)
    except Exception as e:
        logging.exception(e)
        msg = f"error: {e.__class__.__name__}. message: {e}. traceback: {traceback.format_exc()}"
        return {"ok": False, "message": msg}
    
@router.post('/create_cycle_sub')
async def cycle_sub(link_subs: str, version: str, api_key: str, host: str, endpoint: str = None):
    try:    
        asyncio.create_task(event_job_subscription(link_subs=link_subs, version=version, api_key=api_key, host=host, endpoint=endpoint))
        logging.info(f"Создан такс успешно для восстановления активных подписок")
        return {
        "status": 200
    }
    except Exception as e:
        logging.error(f"Ошибка создания таска для восстановления активных подписок: {e}")
        return {
        "status": 400
    }
        
    