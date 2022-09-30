from ctypes import resize
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import CURRENT_URL
import decorators
import json

async def send_start_message(bot: Bot, chat_id):
    text = await decorators.get_text(title='start', chat_id=chat_id)
    await bot.send_message(chat_id, text)

async def send_menu(bot: Bot, chat_id):
    text = await decorators.get_text(title='menu text', chat_id=chat_id, button=True)
    keyboard = InlineKeyboardMarkup(row_width=1)
    text2button1 = await decorators.get_text(title='addchat', chat_id=chat_id, button=True)
    text2button2 = await decorators.get_text(title='addchanel', chat_id=chat_id, button=True)
    text2button3 = await decorators.get_text(title='my_chats', chat_id=chat_id, button=True)
    keyboard.add(
        InlineKeyboardButton(text=text2button1, callback_data='new_chat'),  
        InlineKeyboardButton(text=text2button2, callback_data='new_chanel'),  
        InlineKeyboardButton(text=text2button3, callback_data='my_chats') 
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
    text2button = await decorators.get_text(title='addnewgroup', chat_id=chat_id, button=True)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text2button,
            url=f'https://telegram.me/{CURRENT_URL}?startgroup=new'
        )
    )
    await bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)

async def in_developing(bot: Bot, chat_id):
    text = await decorators.get_text(title='in_developing', chat_id=chat_id)
    await bot.send_message(chat_id, text)

async def add_chanel(bot: Bot, chat_id):
    text = await decorators.get_text(title='addchanel', chat_id=chat_id)
    await bot.send_message(chat_id, text)
    
async def my_chats(bot: Bot, chat_id, message_id):
    text = await decorators.get_text(title='my_chats', chat_id=chat_id, button=True)    

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Chanels',
            callback_data='ch'
        )
    )
    await bot.edit_message_text(text, chat_id, message_id)
    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyboard)




async def fprint(text) -> None:
    print(json.dumps(json.loads(str(text)), indent=4))


async def get_chanel_info(title, username, link, description, members_count, chat_id):
    t = await decorators.get_text('title', chat_id, button=True)
    u = await decorators.get_text('username', chat_id, button=True)
    l = await decorators.get_text('link', chat_id, button=True)
    m = await decorators.get_text('memberscount', chat_id, button=True)
    d = await decorators.get_text('description', chat_id, button=True)
    text = f'''
    {title}:
    {u}: {username}
    {l}: {link} 
    {m}: {members_count}
    {d}: {description}
'''
    return text