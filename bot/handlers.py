from aiogram.types import CallbackQuery, Message
from aiogram import Bot
from bot.functions import add_chanel
from states import New_chanel, Edit_black_list, Edit_white_list


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
    
    elif 'CHAT-' in data:
        await functions.chat_config(bot, call)
    
    elif data == 'menu':
        await functions.send_menu(bot, chat_id)

    elif 'White list' in data:
        await functions.white_list(bot, call)

    elif 'Black list' in data:
        await functions.black_list(bot, call)

    elif 'Filter type' in data:
        await functions.filtertypes(bot, call)   
    
    elif 'Timer' in data:
        await functions.timer_black_list(bot, call)

    elif 'TIMES' in data:
        await functions.edit_timer_black_list(bot, call)

    elif 'Copy filter' in data:
        await functions.copy_filter_choice_chat(bot, call)
    
    elif 'copy' in data:
        await functions.copy_filter(bot, call)

    elif 'statuswhitelist' in data:
        await functions.statuswhitelist(bot, call)

    elif 'statusblacklist' in data:
        await functions.statusblacklist(bot, call)

    elif 'Edit wlist' in data:
        await functions.edit_white_list(bot, call)
        group_id = call.data.split('-')[1]
        await decorators.edit_group_id2user(chat_id, group_id)
        await Edit_white_list.data.set()

    elif 'Edit blist' in data:
        await functions.edit_black_list(bot, call)
        group_id = call.data.split('-')[1]
        await decorators.edit_group_id2user(chat_id, group_id)
        await Edit_black_list.data.set()

    elif 'TYPE-' in data:
        await decorators.edit_type(call)
        await functions.filtertypes(bot, call) 

