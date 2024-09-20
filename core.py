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
from database.data_bubble import get_activity_sub, get_bubble_job_request, post_bubble_job_add
import config
from keybods import create_btn
from upwork.models import Job, Job_Advance, Client
from typing import List
import json
from loguru import logger as logging

# Настройка логирования
logging.add("py_log.log", level="DEBUG")

# logging.basicConfig(
#     level=logging.INFO,  # Уровень логирования
#     filename="py_log.log",  # Имя файла для записи логов
#     filemode="w",  # Режим записи: 'w' для перезаписи, 'a' для добавления
#     format="%(asctime)s %(levelname)s %(message)s"  # Формат сообщений
# )
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
        "send_email": false,
        "name": "Python"
    }
}
    """

#------------------------Уведомления----------------------------
#Отправка Telegram уведомление
async def send_telegram(tg_chat_id: str, job: dict, subs: dict):
    link_jon = job.get('link')
    job_link = str(link_jon).replace('jobs/', "").split("/?")[0]
    url = f"https://www.upwork.com/freelance-jobs/apply{job_link}"
    keybord = await create_btn(url)
    text = f"""New JOB Upwork\n\n<b>{job["title"]}</b>\n\n<i>{job["price"]}</i>\n\n{job['description']}\n\n<i>Posted date: {job.get('posted_date')}</i>\n\n\n<b>Subscription ID: {subs['response']['name']}</b>\nSubscription Link: {subs['response']['sub_link']}"""
    await config.bot.send_message(chat_id=tg_chat_id, text=text, reply_markup=keybord, parse_mode = "HTML")
    
#Отправка Endpoint уведомление
async def send_endpoint(job: dict, endpoint: str):
    link_jon = job.get('link')
    job_link = str(link_jon).replace('jobs/', "").split("/?")[0]
    url = f"https://www.upwork.com/freelance-jobs/apply{job_link}"
    async with aiohttp.ClientSession() as session:
        headers ={
            'Authorization': f'Bearer {config.token_n8n}',
            'Content-Type': 'application/json'
        }
        data = {
            'title': job.get("title"),
            'desctiption': job.get("description"),
            'price': job.get("price"),
            'posted_date': job.get("posted_date"),
            'link': url
        }
        try:
            async with session.post(url=endpoint, headers=headers, json=data) as response:
                response.raise_for_status()  # Проверяем статус ответа
                return await response.json()  # Возвращаем JSON-ответ
        except aiohttp.ClientError as e:
            print(f"HTTP error: {e}")
            return None  # Возвращаем None в случае ошибки
        except Exception as e:
            pass
    

#Нотификации
async def send_notification(job: dict, subs: dict):
    endpoin = subs.get("response", {}).get("endpoint")
    
    if endpoin and endpoin != "empty":
        try:
            await send_endpoint(job=job, endpoint=endpoin)
            logging.info(f"Endpoin успешно отправлен на {endpoin}.")
        except Exception as e:
            logging.error(f"Ошибка при отправке Endpoin на {endpoin}: {e}")

    email = subs.get("response", {}).get("email")
    if email and email != "empty":
        try:
            await send_email(job=job, subs=subs)
            logging.info(f"Email успешно отправлен на {email}.")
        except Exception as e:
            logging.error(f"Ошибка при отправке email на {email}: {e}")

    tg = subs.get("response", {}).get("tg_bot_id")
    if tg and tg != "empty":
        try:    
            await send_telegram(tg_chat_id=tg, job=job, subs=subs)
            logging.info(f"Telegram уведомление успешно отправлено в чат {tg}.")
        except Exception as e:
            logging.error(f"Ошибка при отправке Telegram уведомления в чат {tg}: {e}")

#Отправка Емаил
async def send_email(job: dict, subs: dict):

    # Настройки
    from_email = config.from_email  # Ваш адрес электронной почты
    password = config.gmail_pasword  # Ваш пароль (или токен приложения)
    subject = "New Job Upwork"
    body = f"""Job name: {job["title"]}\n\n
                Job Description: {job['description']}\n\n
                Job Price: {job["price"]}
    """
    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = subs['response']['email']
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
#Запуск подписок в момент запуска программы
async def start_subscription():
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
    """
    subs = await get_activity_sub()
    for sub in subs:
        link = sub.get("link")
        api_key = sub.get("api-key")
        asyncio.create_task(event_job_subscription(link_subs=link,version=config.version, api_key=api_key, host=config.host_url))
        
    

#Создание подписки на Работу Upwork
async def event_job_subscription(link_subs: str, version: str, api_key: str, host: str, endpoint: str = ""):
    """_summary_
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
        "send_email": False
    }
}
    
    new_data = [
    {
        "title": "No Code and Automation Web App Development",
        "description": "I am looking to start building a no code MVP starting with a very specific and simple solution for a business I am supporting. \n\nIt involves building a process to track, review, and approve actions.\n\nFull details and scope can be viewed here: https://docs.google.com/document/d/1M366JPNtbA1z62RiyebE8DTLJX3BKJG94s9CT5I2IWo/edit",
        "price": "Hourly: $10.00 - $40.00 ",
        "link": "/jobs/Code-and-Automation-Web-App-Development_~021836328526713298158/?referrer_url_path=/nx/search/jobs/"
    },
    {
        "title": "Bubble.io Developer for Custom CRM",
        "description": "Project Description\nThe mobile application will leverage Bubble.io to educate people with no business background but having visionary ideas through step by step interactive training modules  featuring animated videos. Users will engage with these tasks by implementing them in their own environments and submitting their assignments through the app. The application will also integrate a backend system for customer relationship management (CRM) and database functionalities, ensuring efficient tracking of user progress and task completion.\n\nKey Features\n1.\tAnimated Training Modules: Users will view animated videos for each task, created using Bubble's design tools.\n2.\tTask Implementation: Users can implement tasks on their own and submit assignments via the app's user-friendly interface.\n3.\tExcel Template Management: Each task will include an Excel template that users can fill out and upload through the app.\n4.\tBackend CRM: A robust backend system built on Bubble to manage user data, track progress, and provide analytics.\n5.\tResponsive Design: The app will be optimized for mobile use, ensuring a seamless experience on various devices.\nRequirement Description\nFunctional Requirements\n1.\tUser Authentication:\n•\tImplement user registration and login functionalities using Bubble's built-in authentication features.\n•\tSupport for social media login options if desired.\n2.\tTask Management:\n•\tAbility to browse tasks, displayed in a mobile-friendly format.\n•\tIntegration of animated videos for each task using Bubble's video elements.\n3.\tAssignment Submission:\n•\tUsers can upload completed Excel templates directly through the app.\n•\tProvide submission confirmation and feedback mechanisms.\n4.\tProgress Tracking:\n•\tDashboard for users to view completed tasks and assignments, utilizing Bubble's data display capabilities.\n•\tVisual representation of progress through charts or graphs created within Bubble.\n5.\tNotifications:\n•\tPush notifications for new tasks, reminders for pending assignments, and updates using Bubble's notification features.\nNon-Functional Requirements\n1.\tPerformance:\n•\tThe app should load content quickly, ideally within 2 seconds, leveraging Bubble's optimization tools.\nSecurity:\n•\tEnsure user data is encrypted during transmission and storage using Bubble's security features.\n•\tCompliance with data protection regulations (e.g., GDPR).\nUsability:\n•\tThe interface must be intuitive, designed with responsive editing in Bubble to accommodate various screen sizes.\nCompatibility:\n•\tThe app should be compatible with both iOS and Android platforms through wrapping solutions like BDK or Natively if necessary.\nTechnical Requirements\nDevelopment Tools:\nUtilize Bubble.io as the primary development platform for building both web and mobile components of the app.\nMobile Wrapping Solutions:\nConsider using wrappers like BDK or Natively to convert the Bubble web app into a native mobile app for distribution on app stores if needed.\nAPIs:\nIntegrate necessary APIs for handling file uploads (Excel templates) securely within the Bubble environment.\nTesting:\nImplement a testing strategy that includes unit tests, integration tests, and user acceptance testing (UAT) within the Bubble framework.",
        "price": "Hourly",
        "link": "/jobs/span-class-highlight-Bubble-span-Developer-for-Custom-CRM_~021836324357197634798/?referrer_url_path=/nx/search/jobs/"
    },

    Args:
        url (str): _description_
        version (str): _description_
        link (str): _description_
        api_key (str): _description_
    """
    while True:
        logging.info(f"Начался цикл с подпиской")
        #Получение данных из Bubble
        host_url = f"{host}version-{version}/api/1.1/wf/"
        try:
            subs = await get_bubble_job_request(host_url=host_url, api_key=api_key,link=link_subs)
        except Exception as e:
            logging.error(f"Не смогли получить даннеые из Bubble {link_subs}: {e}")
        if subs.get("response", {}).get("subscription_status") != "ACTIVE":
            break
        
        token_bubble = config.token_bubble
        data_notification = []
        #Получение данных из Upwork
        try:
            new_data = await get_info_list(link_subs)
        except Exception as e:
            logging.error(f"Не смогли получить даннеые из Upwork: {e}")
            new_data = []
        
    
        # Проверяем наличие новых объектов по полю "link"
        
        if subs:
            old_links = {jobs['link'] for jobs in subs["response"]["jobs"]}
            # Фильтруем новые данные
            for job_new in new_data:
                if job_new['link'] not in old_links:  # Проверяем, есть ли ссылка в old_links
                    data_notification.append(job_new)  # Добавляем новые объекты в data_notification
                    # Здесь можно обработать data_notification (например, отправить уведомление)
                    try:
                        await post_bubble_job_add(host=host_url, api_key=api_key, token_bubble=token_bubble, job=job_new, subs=subs)
                        logging.info(f"Работа добавлена: {job_new}")
                    except Exception as e:
                        logging.error(f"Не смогли добавить работу: {e}")    
                    await send_notification(job=job_new, subs=subs)
                    
                   
        duration = int(config.duration)
        # Задержка перед следующим запросом
        logging.info(f"Цикл успешно закончился подписка: {subs['response']['sub_id']}")
        await asyncio.sleep(duration)  # Задержка перед следующим запросом

