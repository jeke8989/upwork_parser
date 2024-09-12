import traceback
from fastapi import APIRouter
from core import get_info_list, get_single_job
from loguru import logger

router = APIRouter()

@router.get('/list_jobs')
async def get_list_jobs_upwork(url: str):
    try:
        return await get_info_list(url=url)
    except Exception as e:
        logger.exception(e)
        msg = f"error: {e.__class__.__name__}. message: {e}. traceback: {traceback.format_exc()}"
        return {"ok": False, "message": msg}
        
    
@router.get('/job')
async def get_job_upwork(url: str):
    try:
        return await get_single_job(url=url)
    except Exception as e:
        logger.exception(e)
        msg = f"error: {e.__class__.__name__}. message: {e}. traceback: {traceback.format_exc()}"
        return {"ok": False, "message": msg}