from dotenv import load_dotenv
from aiogram import Bot
import os

load_dotenv('.env')
token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token)

token_bubble =  os.getenv("TOKEN_BUBBLE")
duration = os.getenv("DURATION")
