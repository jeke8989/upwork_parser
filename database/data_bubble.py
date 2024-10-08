
import aiohttp
import config
# from loguru import logger as logging
from loguru import logger
import config
import json
# logging.add("py_log.log", level="DEBUG")


#------------------------Bubble Requests----------------------------
#https://web-scraping-gdn.bubbleapps.io/version-test/api/1.1/wf/create_job/initialize
#Получение данных по одному юзеру 
async def get_bubble_job_request(api_key: str, link: str) -> dict:
    host_url_job = f"{config.host_url_restart}get_jobs"
    async with aiohttp.ClientSession() as session:
        header ={
            'Authorization': f'Bearer {config.token_bubble}',
            'Content-Type': 'application/json'
        }
        params = {
            'api_key': api_key,
            'link': link
        }
        try:
            async with session.get(host_url_job, headers=header, params=params) as respose:
                respose.raise_for_status()
                data = await respose.json()
                return data
                
        except aiohttp.ClientError as e:
            return logger.error(f"{e}")
        except Exception as e:
            return logger.error(f"{e}")

#Запись новых работ в базу данных
async def post_bubble_job_add(api_key: str, token_bubble: str, job: dict, subs: dict):
    #host_url_job = "https://web-scraping-gdn.bubbleapps.io/version-test/api/1.1/wf/create_job/initialize"
    host_url_job = f"{config.host_url_restart}create_job"
    async with aiohttp.ClientSession() as session:
        headers ={
            'Authorization': f'Bearer {token_bubble}',
            'Content-Type': 'application/json'
        }
        data = {
            'api_key': api_key,
            'job': job,
            'link': subs['response']['sub_link']
        }
        try:
            async with session.post(url=host_url_job, headers=headers, json=data) as response:
                response.raise_for_status()  # Проверяем статус ответа
                n = response.json()
                logger.info(f"Работа успешно добавлена.")
                return await n  # Возвращаем JSON-ответ
        except aiohttp.ClientError as e:
            print(f"HTTP error: {e}")
            return None  # Возвращаем None в случае ошибки
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Возвращаем None в случае ошибки

#Получение всех активных подписок для запуска при рестарте приложения
async def get_activity_sub() -> dict:
    
    """_summary_
    [
  {
    "link": "https://www.upwork.com/nx/search/jobs/?q=bubble",
    "api-key": "1111"
  },
  {
    "link": "https://www.upwork.com/nx/search/jobs/?nbs=1",
    "api-key": "2222"
  }
]

    Returns:
        _type_: _description_
    """

    host_url_job = f"{config.host_url_restart}get_all_status_sub"
    
    
    async with aiohttp.ClientSession() as session:
        header ={
            'Authorization': f'Bearer {config.token_bubble}',
            'Content-Type': 'application/json'
        }
        try:
            async with session.post(host_url_job, headers=header) as respose:
                respose.raise_for_status()
                data = await respose.json()
                # Получаем ссылки и api_key
                links = data["response"]["link"]
                api_keys = data["response"]["api_key"]

                # Создаем новый объект
                result = [{"link": link, "api-key": api_key} for link, api_key in zip(links, api_keys)]
                logger.info(f"Получение всех активных подписок для запуска при рестарте приложения.")
                return result
        except aiohttp.ClientError as e:
            return logger.error(f"{e}")
        except Exception as e:
            return logger.error(f"{e}")