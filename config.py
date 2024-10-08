from dotenv import load_dotenv
from aiogram import Bot
import os

load_dotenv('.env')
token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token)

token_bubble =  os.getenv("TOKEN_BUBBLE")
duration = os.getenv("DURATION")
from_email = os.getenv("FROM_EMAIL")
gmail_pasword = os.getenv("APP_GOOGLE_PASSWORD")
token_n8n = os.getenv("TOKEN_N8N")
host_url_restart = os.getenv("HOST_URL_RESTART")
host_url = os.getenv("HOST_URL")
version = os.getenv("VERSION")

