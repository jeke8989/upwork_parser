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

from config import bot
from keybods import create_btn
from upwork.models import Job, Job_Advance, Client
from typing import List


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


async def get_info_list(url: str):
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
async def get_single_job_old(url: str):
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


async def get_single_job(url: str):
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
