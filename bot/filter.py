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
        keys = group.white_list
    elif group.enable_black_list:
        keys = group.black_list.split('&')
        print(keys)
        if len(keys) == 1 and keys[0] == '-':
            return False
        return True if text in keys else True
    return False


async def handler(bot: Bot, message: Message):
    await fprint(message)

async def chanel_handler(bot: Bot, message: Message):
    chat_id = message.chat.id
    text = message.text if 'text' in message.iter_keys() else message.caption if 'caption' in message.iter_keys() else False
    if text:
        status = await check_filter(chat_id, text)
        if status:
            await bot.delete_message(chat_id, message.message_id)