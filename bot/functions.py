from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import CURRENT_URL
import decorators

async def send_start_message(bot: Bot, chat_id):
    text = await decorators.get_text(title='start', chat_id=chat_id)
    await bot.send_message(chat_id, text)

async def send_menu(bot: Bot, chat_id):
    text = await decorators.get_text(title='menu text', chat_id=chat_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Подключить новый чат', callback_data='new_chat'),  
        InlineKeyboardButton(text='Подключённые чаты', callback_data='my_chats') 
    )
    await bot.send_message(chat_id, text, reply_markup=keyboard)

async def send_language_post(bot: Bot, chat_id):
    text = await decorators.get_text(title='select language', chat_id=chat_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Русский🇷🇺', callback_data='ru'),  
        InlineKeyboardButton(text='English🏴󠁧󠁢󠁥󠁮󠁧󠁿', callback_data='eng') 
    )
    await bot.send_message(chat_id, text, reply_markup=keyboard)

async def send_post_add_new_chat(bot: Bot, chat_id):
    text = await decorators.get_text(title='select language', chat_id=chat_id)
    text2button = await decorators.get_text(title='addnewgroup', chat_id=chat_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text2button,
            url=f'https://telegram.me/{CURRENT_URL}?startgroup=new'
        )
    )
    await bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
