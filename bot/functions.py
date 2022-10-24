from ctypes import resize
from pickle import decode_long
from re import T
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


from config import CURRENT_URL
import decorators
import json

async def send_start_message(bot: Bot, chat_id) -> None:
    text = await decorators.get_text(title='start', chat_id=chat_id)
    await bot.send_message(chat_id, text)

async def send_menu(bot: Bot, chat_id) -> None:
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

async def send_language_post(bot: Bot, chat_id) -> None:
    text = await decorators.get_text(title='select language', chat_id=chat_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Русский🇷🇺', callback_data='ru'),  
        InlineKeyboardButton(text='English🏴󠁧󠁢󠁥󠁮󠁧󠁿', callback_data='eng') 
    )
    await bot.send_message(chat_id, text, reply_markup=keyboard)

async def send_post_add_new_chat(bot: Bot, chat_id) -> None:
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

async def in_developing(bot: Bot, chat_id) -> None:
    text = await decorators.get_text(title='in_developing', chat_id=chat_id)
    await bot.send_message(chat_id, text)

async def add_chanel(bot: Bot, chat_id) -> None:
    text = await decorators.get_text(title='addchanel', chat_id=chat_id)
    await bot.send_message(chat_id, text)
    
async def my_chats(bot: Bot, chat_id, message_id) -> None:
    text = await decorators.get_text(title='my_chats', chat_id=chat_id, button=True)   

    keyboard = InlineKeyboardMarkup()
    buttons = await decorators.get_list_chats(chat_id)
    for group in buttons:
        keyboard.add(
            InlineKeyboardButton(
                text=group.title,
                callback_data=f'CHAT-{group.id}'
            )
        )
    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data='menu'
            )
        )    
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

async def fprint(text) -> None:
    print(json.dumps(json.loads(str(text)), indent=4))

async def get_chanel_info(title, username, link, description, members_count, chat_id):
    u = await decorators.get_text('username', chat_id, button=True)
    l = await decorators.get_text('link', chat_id, button=True)
    m = await decorators.get_text('memberscount', chat_id, button=True)
    d = await decorators.get_text('description', chat_id, button=True)
    
    return f'{title}:\n\t{u}: {username}\n\t{l}: {link}\n\t{m}: {members_count}\n\t{d}: {description}'

async def chat_config(bot: Bot, call) -> None:
    chat_id = call.from_user.id
    message_id = call.message.message_id
    group_id = call.data.split('-')[1]
    group = await decorators.get_group(group_id)
    text = await get_chanel_info(
        title=group.title,
        username=group.username,
        link=group.link,
        description=group.description,
        members_count=group.users_count,
        chat_id=chat_id
    )
    keyboard = InlineKeyboardMarkup(row_width=1)  

    text2button1 = await decorators.get_text(title='White list', chat_id=chat_id, button=True)
    text2button2 = await decorators.get_text(title='Black list', chat_id=chat_id, button=True)
    text2button3 = await decorators.get_text(title='Copy filter', chat_id=chat_id, button=True)

    keyboard.add(
            InlineKeyboardButton(
                text=text2button1,
                callback_data=f'White list-{group_id}'
            ),
            InlineKeyboardButton(
                text=text2button2,
                callback_data=f'Black list-{group_id}'
            ),
            InlineKeyboardButton(
                text=text2button3,
                callback_data=f'Copy filter-{group_id}'
            )
        )
    
    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data='my_chats'
            )
        ) 
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)
    #await bot.edit_message_reply_markup(chat_id, message_id)

async def white_list(bot: Bot, call) -> None:
    chat_id = call.from_user.id
    message_id = call.message.message_id
    group_id = int(call.data.split('-')[1])
    group = await decorators.get_group(group_id)
    text = group.white_list
    keyboard = InlineKeyboardMarkup(row_width=1)  

    text2button = await decorators.get_text(title='Edit white list', chat_id=chat_id, button=True)

    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'Edit wlist-{group_id}'
            )
        )
    if group.enable_white_list:
        text2button = await decorators.get_text(title='on', chat_id=chat_id, button=True)
    else:
        text2button = await decorators.get_text(title='off', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'statuswhitelist-{group.id}:{text2button}'
            )
        )

    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'CHAT-{group.id}'
            )
        )
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

async def black_list(bot: Bot, call) -> None:
    chat_id = call.from_user.id
    message_id = call.message.message_id
    group_id = int(call.data.split('-')[1])
    group = await decorators.get_group(group_id)
    text = group.black_list
    keyboard = InlineKeyboardMarkup(row_width=1)  

    text2button = await decorators.get_text(title='Edit black list', chat_id=chat_id, button=True)

    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'Edit blist-{group_id}'
            )
        )
    
    text2button = await decorators.get_text(title='Timer', chat_id=chat_id, button=True)
    keyboard.add(InlineKeyboardButton(text=text2button,callback_data=f'Timer-timer:{group_id}'))
    if group.enable_black_list:
        text2button = await decorators.get_text(title='on', chat_id=chat_id, button=True)
    else:
        text2button = await decorators.get_text(title='off', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'statusblacklist-{group.id}:{text2button}'
            )
        )
    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'CHAT-{group.id}'
            )
        )
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

async def timer_black_list(bot: Bot, call) -> None:
    chat_id = call.from_user.id
    message_id = call.message.message_id
    data, group_id = call.data.split('-')[1].split(':')
    group_id = int(group_id)
    group = await decorators.get_group(group_id)
    text = await decorators.get_text(title='edit timer', chat_id=chat_id)
    keyboard = InlineKeyboardMarkup(row_width=5)
    times = {0: '0', 10: '10', 20: '20', 30: '30', 60: '60', group.black_list_timer: f'{group.black_list_timer}✅'}
    keyboard.add(*[InlineKeyboardButton(text=i, callback_data=f'TIMES-{i}:{group_id}') for i in times.values()])

    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'Black list-{group_id}'
            )
        )
    
            
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

async def edit_timer_black_list(bot: Bot, call) -> None:
    data, group_id = call.data.split('-')[1].split(':')
    if '✅' not in data:
        await decorators.set_group_bl_timer(int(data), int(group_id))
        await timer_black_list(bot, call)

async def copy_filter_choice_chat(bot: Bot, call):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    text = await decorators.get_text(title='copy filter', chat_id=chat_id)   
    group_id = int(call.data.split('-')[1])

    keyboard = InlineKeyboardMarkup()
    buttons = await decorators.get_list_chats(chat_id)
    for gr in buttons:
        if int(gr.id) != group_id:
            keyboard.add(
                InlineKeyboardButton(
                    text=gr.title,
                    callback_data=f'copy-{gr.id}:{group_id}'
                )
            )
    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'CHAT-{group_id}'
            )
        )   
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

async def copy_filter(bot: Bot, call):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    from_group_id, group_id = call.data.split('-')[1].split(':')
    await decorators.copy_filter(from_group_id, group_id)
    group = await decorators.get_group(group_id)
    text = await get_chanel_info(
        title=group.title,
        username=group.username,
        link=group.link,
        description=group.description,
        members_count=group.users_count,
        chat_id=chat_id
    )
    keyboard = InlineKeyboardMarkup(row_width=1)  

    text2button1 = await decorators.get_text(title='White list', chat_id=chat_id, button=True)
    text2button2 = await decorators.get_text(title='Black list', chat_id=chat_id, button=True)
    text2button3 = await decorators.get_text(title='Copy filter', chat_id=chat_id, button=True)

    keyboard.add(
            InlineKeyboardButton(
                text=text2button1,
                callback_data=f'White list-{group_id}'
            ),
            InlineKeyboardButton(
                text=text2button2,
                callback_data=f'Black list-{group_id}'
            ),
            InlineKeyboardButton(
                text=text2button3,
                callback_data=f'Copy filter-{group_id}'
            )
        )
    
    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data='my_chats'
            )
        ) 
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

async def statuswhitelist(bot: Bot, call):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    group_id, data = call.data.split('-')[1].split(':')
    text = await decorators.edit_status_white_and_black_lists(group_id, 'white', data, chat_id)
    if text:
        await bot.send_message(chat_id, text)
    group = await decorators.get_group(id=group_id)

    keyboard = InlineKeyboardMarkup(row_width=1)  

    text2button = await decorators.get_text(title='Edit white list', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'Edit wlist-{group_id}'
            )
        )
    if group.enable_white_list:
        text2button = await decorators.get_text(title='on', chat_id=chat_id, button=True)
    else:
        text2button = await decorators.get_text(title='off', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'statuswhitelist-{group.id}:{text2button}'
            )
        )

    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'CHAT-{group.id}'
            )
        )
    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyboard)

async def statusblacklist(bot: Bot, call):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    group_id, data = call.data.split('-')[1].split(':')
    text = await decorators.edit_status_white_and_black_lists(group_id, 'black', data, chat_id)
    if text:
        await bot.send_message(chat_id, text)
    group = await decorators.get_group(group_id)

    keyboard = InlineKeyboardMarkup(row_width=1)  

    text2button = await decorators.get_text(title='Edit black list', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'Edit blist-{group_id}'
            )
        )
    text2button = await decorators.get_text(title='Timer', chat_id=chat_id, button=True)
    keyboard.add(InlineKeyboardButton(text=text2button,callback_data=f'Timer-timer:{group_id}'))
    if group.enable_black_list:
        text2button = await decorators.get_text(title='on', chat_id=chat_id, button=True)
    else:
        text2button = await decorators.get_text(title='off', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'statusblacklist-{group.id}:{text2button}'
            )
        )
    text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
    keyboard.add(
            InlineKeyboardButton(
                text=text2button,
                callback_data=f'CHAT-{group.id}'
            )
        )
    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyboard)

async def edit_white_list(bot: Bot, call):
    chat_id = call.from_user.id
    group_id = call.data.split('-')[1]
    text = await decorators.get_group_wlist(id = group_id)
    await bot.send_message(chat_id, text)
    message_id = call.message.message_id
    text = await decorators.get_text(title='edit white or black list', chat_id=chat_id)
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=InlineKeyboardMarkup())

async def edit_black_list(bot: Bot, call):
    chat_id = call.from_user.id
    group_id = call.data.split('-')[1]
    text = await decorators.get_group_blist(id = group_id)
    await bot.send_message(chat_id, text)
    message_id = call.message.message_id
    text = await decorators.get_text(title='edit white or black list', chat_id=chat_id)
    await bot.edit_message_text(text, chat_id, message_id, reply_markup=InlineKeyboardMarkup())