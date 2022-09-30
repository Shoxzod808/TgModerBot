from aiogram.types import CallbackQuery, Message
from aiogram import Bot
from bot.functions import add_chanel
from states import New_chanel


import decorators
import functions



async def print_msg(func, text):
    print(f'from modul handlers({func}) -> ', text)


async def callback_query(bot: Bot, call: CallbackQuery):
    chat_id = call.from_user.id
    data = call.data
    if not await decorators.exists(chat_id):
        await call.message.delete()
        await decorators.add_user(call)
        await functions.send_language_post(bot, chat_id)
    elif data in ['ru', 'eng']:
        await call.message.delete()
        await decorators.set_user_language(chat_id, data)
        await functions.send_start_message(bot, chat_id)
        await functions.send_menu(bot, chat_id)
    
    elif data == 'new_chat':
        await functions.send_post_add_new_chat(bot, chat_id)

    elif data == 'new_chanel':
        await add_chanel(bot, chat_id)
        await New_chanel.info.set()
    
    elif data == 'my_chats':
        await functions.my_chats(bot, chat_id, call.message.message_id)
        
    

async def handler(bot: Bot, message: Message):
    pass
    
