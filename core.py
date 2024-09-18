import asyncio
import aiohttp
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from playwright.async_api import async_playwright
from playwright_stealth.stealth import stealth_async
from soupsieve import select_one
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import bot
import config
from keybods import create_btn
from upwork.models import Job, Job_Advance, Client
from typing import List
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
# Получение окружения
load_dotenv('.env')


#------------------------Парсинг Upwork----------------------------
# Запрашиваем работы из Upwork списком
async def get_info_list_upwork(url: str):
    driver = webdriver.Chrome()
    driver.get(url)

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-tile")
    for index, i in enumerate(job_elements):
        # Найти заголовок вакансии по имени класса
        title = i.find_element(By.CLASS_NAME, "job-tile-title")

        # Найти элемент <a> внутри заголовка
        link_element = title.find_element(By.TAG_NAME, "a")

        # Извлечь ссылку (атрибут href) из элемента <a>
        link = link_element.get_attribute("href")

        # Найти элемент с атрибутом data-test
        price = i.find_element(By.CSS_SELECTOR, '[data-test="job-type-label"]')

        # Найти описание вакансии по имени класса

        description = i.find_element(By.CLASS_NAME, "text-body-sm")

        # Печать найденных текстов
        text_message = (
            f"<b>{title.text}</b>\n\n<i>{price.text}</i>\n\n{description.text[0:350]}"
        )

        await bot.send_message(
            chat_id="-1002100619620",
            text=text_message,
            reply_markup=await create_btn(url=link),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    driver.close()

# Получаем лист работ в класссе Job
async def get_info_list_old(url: str):
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Ждем загрузки страницы (максимум 10 секунд)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-tile")))

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-tile")

    job_list = []

    for index, i in enumerate(job_elements):
        # Найти заголовок вакансии по имени класса
        title = i.find_element(By.CLASS_NAME, "job-tile-title")

        # Найти элемент <a> внутри заголовка
        link_element = title.find_element(By.TAG_NAME, "a")

        # Извлечь ссылку (атрибут href) из элемента <a>
        link = link_element.get_attribute("href")

        # Найти элемент с атрибутом data-test
        price = i.find_element(By.CSS_SELECTOR, '[data-test="job-type-label"]')

        # Найти описание вакансии по имени класса

        description = i.find_element(By.CLASS_NAME, "text-body-sm")
        job_append = Job(
            id=index + 1,
            title=title.text,
            description=description.text,
            price=price.text,
            link=link,
        )
        job_list.append(job_append.to_dict())

    driver.close()
    return job_list

async def get_info_list(url: str) -> dict:
    proxy = "http://185.162.130.85:10005"
    proxy_username = "JfhR3aez3sSp"
    proxy_password = "RNW78Fm5"
    job_list = []

    def parse_with_soup(tag: bs4.Tag, index: int):
        nonlocal job_list

        title = tag.select_one(".job-tile-title")
        link_element = tag.select_one("a")
        link = link_element["href"]
        price = tag.select_one('[data-test="job-type-label"]')
        description = tag.select_one(".text-body-sm")

        job_append = Job(
            id=index + 1,
            title=title.text,
            description=description.text,
            price=price.text,
            link=link,
        )
        job_list.append(job_append.to_dict())

    async with async_playwright() as plw:
        browser = await plw.chromium.launch(headless=False)
        context = await browser.new_context(
            proxy={
                "server": proxy,
                "username": proxy_username,
                "password": proxy_password,
            }
        )
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(url, wait_until="domcontentloaded")
        content = await page.content()

    soup = bs4.BeautifulSoup(content, "lxml")
    job_elements = soup.select(".job-tile")

    tasks = []
    for index, i in enumerate(job_elements):
        i: bs4.Tag
        tasks.append(asyncio.to_thread(parse_with_soup, i, index))

    await asyncio.gather(*tasks)

    return job_list

# Получаем данные по одной работе
async def get_single_job_old(url: str) -> dict:
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Ждем загрузки страницы (максимум 10 секунд)
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="client-location"]'))
    )
    # Получаем данные по клиенту
    try:
        client_location = (
            driver.find_element(By.CSS_SELECTOR, '[data-qa="client-location"]')
            .find_element(By.TAG_NAME, "strong")
            .text
        )
    except Exception as e:
        client_location = ""
    try:
        client_job_posted = (
            driver.find_element(By.CSS_SELECTOR, '[data-qa="client-job-posting-stats"]')
            .find_element(By.TAG_NAME, "strong")
            .text
        )
    except Exception as e:
        client_job_posted = ""
    try:
        client_job_rate = (
            driver.find_element(By.CSS_SELECTOR, '[data-qa="client-job-posting-stats"]')
            .find_element(By.TAG_NAME, "div")
            .text
        )
    except Exception as e:
        client_job_rate = ""
    client = Client(
        location=client_location, job_info=client_job_posted, job_rate=client_job_rate
    )

    # Получаем данные по работе

    header = driver.find_element(By.CSS_SELECTOR, ".air3-card-section")
    title = header.find_element(By.TAG_NAME, "h4")
    posted_date = header.find_element(By.TAG_NAME, "span")

    location = header.find_element(By.CSS_SELECTOR, '[data-test="LocationLabel"]')

    description = driver.find_element(By.CSS_SELECTOR, '[data-test="Description"]')

    # Получаем все элементы с атрибутом data-test="BudgetAmount"
    budget_elements = driver.find_elements(
        By.CSS_SELECTOR, '[data-test="BudgetAmount"]'
    )

    # Извлекаем текст из каждого элемента
    budget_texts = [element.text for element in budget_elements]

    # Объединяем текст с помощью join
    result = " - ".join(budget_texts)

    job_advance = Job_Advance(
        client=client,
        title=title.text,
        description=description.text,
        link=url,
        price=result,
        posted_date=posted_date.text,
        location_freelancer=location.text,
    )

    driver.close()
    return job_advance.to_dict()


async def get_single_job(url: str) -> dict:
    proxy = "http://185.162.130.85:10005"
    proxy_username = "JfhR3aez3sSp"
    proxy_password = "RNW78Fm5"

    async with async_playwright() as plw:
        browser = await plw.chromium.launch(headless=False)
        context = await browser.new_context(
            proxy={
                "server": proxy,
                "username": proxy_username,
                "password": proxy_password,
            }
        )
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(url, wait_until="domcontentloaded")
        
        await page.mouse.wheel(0, 15000)
        await asyncio.sleep(3)
        
        content = await page.content()

    soup = bs4.BeautifulSoup(content, "lxml")

    # Получаем данные по клиенту
    try:
        client_location = (
            soup.select_one('[data-qa="client-location"]')
            .select_one("strong").text
        )
    except Exception as e:
        client_location = ""
    try:
        client_job_posted = (
            soup.select_one('[data-qa="client-job-posting-stats"]').select_one("strong")
            .text
        )
    except Exception as e:
        client_job_posted = ""
    try:
        client_job_rate = (
            soup.select_one('[data-qa="client-job-posting-stats"]')
            .select_one("div")
            .text
        )
    except Exception as e:
        client_job_rate = ""
        
    client = Client(
        location=client_location, job_info=client_job_posted, job_rate=client_job_rate
    )

    # Получаем данные по работе

    header = soup.select_one(".air3-card-section")
    title = header.select_one("h4")
    posted_date = header.select_one("span")

    location = header.select_one('span[data-v-d0a8572a]')

    description = soup.select_one('p[data-v-60ea767b]')

    # Получаем все элементы с атрибутом data-test="BudgetAmount"
    budget_elements = soup.select('strong[data-v-8d6ae40e]')

    # Извлекаем текст из каждого элемента
    budget_texts = [element.get_text(strip=True) for element in budget_elements]

    # Объединяем текст с помощью join
    result = " - ".join(budget_texts)

    job_advance = Job_Advance(
        client=client,
        title=title.get_text(strip=True),
        description=description.get_text(strip=True),
        link=url,
        price=result,
        posted_date=posted_date.get_text(strip=True),
        location_freelancer=location.get_text(strip=True),
    )

    return job_advance.to_dict()
#------------------------Запросы в Bubble----------------------------

#Запрос работ в Bubble по API ключу
    """_subs: - dict - example_
    {
    "status": "success",
    "response": {
        "stasus": 200,
        "jobs": [
            {
                "Created Date": 1726610370469,
                "Subscribe": "1726609240472x770120660674471300",
                "Created By": "admin_user_web-scraping-gdn_test",
                "Modified Date": 1726610370470,
                "client_job_info": "323",
                "client_job_rate": "32",
                "client_location": "323",
                "description": "323",
                "link": "323",
                "location_freelancer": "32",
                "posted_date": "323",
                "price": "32",
                "title": "323",
                "_id": "1726610370468x816143841096277400"
            }
        ],
        "sub_link": "https://www.upwork.com/nx/search/jobs/?q=bubble",
        "sub_id": "42452523",
        "subscription_status": "ACTIVE",
        "send_email": false
    }
}
    """

#------------------------Bubble Requests----------------------------

async def get_bubble_job_request(host_url: str, api_key: str, token_bubble: str, link: str) -> dict:

    async with aiohttp.ClientSession() as session:
        header ={
            'Authorization': f'Bearer {token_bubble}',
            'Content-Type': 'application/json'
        }
        param = {
            'api_key': api_key,
            'link': link
        }
        try:
            async with session.get(host_url, headers=header, params=param) as respose:
                respose.raise_for_status()
                data = await respose.json()
                return data
        except aiohttp.ClientError as e:
            print(f"HTTP error: {e}")
            return None  # Возвращаем None в случае ошибки
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Возвращаем None в случае ошибки


#------------------------Уведомления----------------------------
#Отправка Telegram уведомление
async def send_telegram(tg_chat_id: str, job: dict, subs: dict):
    url = job['link']
    keybord = await create_btn(url)
    text = f"""New JOB Upwork\n\n<b>{job["title"]}</b>\n\n<i>{job["price"]}</i>\n\n{job['description']}\n\n<i>Posted date: {job['posted_date']}</i>\n\n\n<b>Subscription ID: {subs['response']['sub_id']}</b>\nSubscription Link: {subs['response']['sub_link']}"""
    await config.bot.send_message(chat_id=tg_chat_id, text=text, reply_markup=keybord, parse_mode = "HTML")

#Нотификации
async def send_notification(email: str, job: dict, subs: dict, tg_bot_id: str = ""):
        try:
            await send_email(to_email=email, job=job, subs=subs)
            logging.info(f"Email успешно отправлен на {email}.")
        except Exception as e:
            logging.error(f"Ошибка при отправке email на {email}: {e}")
        try:    
            if tg_bot_id != "":
                await send_telegram(tg_chat_id=tg_bot_id, job=job, subs=subs)
                logging.info(f"Telegram уведомление успешно отправлено в чат {tg_bot_id}.")
        except Exception as e:
            logging.error(f"Ошибка при отправке Telegram уведомления в чат {tg_bot_id}: {e}")

#Отправка Емаил
async def send_email(job: dict, subs: dict, to_email: str):

    # Настройки
    from_email = os.getenv("FROM_EMAIL")  # Ваш адрес электронной почты
    password = os.getenv("APP_GOOGLE_PASSWORD")  # Ваш пароль (или токен приложения)
    subject = "New Job Upwork"
    body = f"""Job name: {job["title"]}\n\n
                Job Description: {job['description']}\n\n
                Job Price: {job["price"]}
    """
    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Добавление текста в сообщение
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Подключение к серверу Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Начало шифрования
        server.login(from_email, password)  # Аутентификация

        # Отправка сообщения
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        server.quit()  # Закрытие соединения


#------------------------Локика Зацикливания Уведомлений----------------------------


#Создание подписки на Работу Upwork
async def event_job_subscription(url: str, version: str, link: str, api_key: str):
    while True:
        new_data = await get_info_list(url)
        email_subscriber = new_data["email"]
        tg_bot_id = new_data["tg_bot_id"]
        if new_data["subscription_status"] == "STOP":
            break
        # Логика проверки на новые данные
        token_bubble = os.getenv('TOKEN_BUBBLE')
        host_url = f"https://web-scraping-gdn.bubbleapps.io/version-{version}/api/1.1/wf/get_jobs"
        old_data = await get_bubble_job_request(host_url=host_url, api_key=api_key, token_bubble=token_bubble,link=link)
        # Проверяем наличие новых объектов по полю "link"
        data_notification = []
        if old_data:
            old_links = {jobs['link'] for jobs in old_data}
            # Фильтруем новые данные
            for job in new_data:
                if job[' link'].strip() not in old_links:  # Проверяем, есть ли ссылка в old_links
                    data_notification.append(job)  # Добавляем новые объекты в data_notification
                    # Здесь можно обработать data_notification (например, отправить уведомление)
                    await send_notification(email=email_subscriber, tg_bot_id=tg_bot_id, job=job)
                    
       
        # Задержка перед следующим запросом
        await asyncio.sleep(config.duration)  # Задержка перед следующим запросом

