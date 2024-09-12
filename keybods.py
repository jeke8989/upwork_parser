from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import bot




async def create_btn(url: str) -> InlineKeyboardMarkup:
    key_link = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Open link", url=url)]
        ])
    return key_link  

