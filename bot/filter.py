from aiogram import Bot
from aiogram.types import Message
from asgiref.sync import sync_to_async
import config
from backend.models import Group, BotUser
from functions import fprint

@sync_to_async
def check_filter(chat_id, text) -> bool:
    group = Group.objects.filter(chat_id=chat_id)
    if not group.exists():
        return False
    group = group[0]
    if group.enable_white_list:
        keys = group.white_list.split('&')
        return all(key.strip().lower() not in text.lower() for key in keys)

    elif group.enable_black_list:
        keys = group.black_list.split('&')
        if len(keys) == 1 and keys[0] == '-':
            return False
        for key in keys:

            if key.strip().lower() in text.lower():
                return True
    return False

async def handler(bot: Bot, message: Message):
    chat_id = message.chat.id
    text = message.text if 'text' in message.iter_keys() else message.caption if 'caption' in message.iter_keys() else False
    if text:
        status = await check_filter(chat_id, text)
        if status:
            await bot.delete_message(chat_id, message.message_id)