from aiogram import Bot
from aiogram.types import Message
from asgiref.sync import sync_to_async
import config
from backend.models import Group, BotUser
from functions import fprint
import asyncio

@sync_to_async
def get_group(message):
    chat_id = message.chat.id
    group = Group.objects.get(chat_id=chat_id)
    return group

@sync_to_async
def checkgroup(message):
    group = Group.objects.filter(chat_id=message.chat.id)
    if not group.exists():
        return False
    return True

@sync_to_async
def check_hidden_links(chat_id, message):
    group = Group.objects.get(chat_id=message.chat.id)
    if not group.filter_link_in_text:
        return True
    try:
        message['entities'][0].url
        return False
    except Exception as e:
        pass
    return True


@sync_to_async
def check_filter(chat_id, text) -> bool:
    group = Group.objects.filter(chat_id=chat_id)
    if not group.exists():
        return (False, 0)
    group = group[0]
    if group.enable_white_list:
        keys = group.white_list.split('\n')
        if all(key.strip().lower() not in text.lower() for key in keys):
            return (True, 0)
    if group.enable_black_list:
        keys = group.black_list.split('\n')
        if len(keys) == 1 and keys[0] == '-':
            return (False, 0)
        for key in keys:
            if key.strip().lower() in text.lower():
                return (True, group.black_list_timer)
    return (False, 0)

async def handler(bot: Bot, message: Message):
    chat_id = message.chat.id
    types = []
    text = message.text if 'text' in message.iter_keys() else message.caption if 'caption' in message.iter_keys() else False
    if await checkgroup(message):
        group = await get_group(message)
        if group.filter_photo:
            types.append('photo')
            types.append('animation')
        if group.filter_text:
            types.append('text')
        if group.filter_voice:
            types.append('voice')
            types.append('audio')
        if group.filter_video_note:
            types.append('video_note')
        if group.filter_video:
            types.append('video')
        if group.filter_document:
            types.append('document')
        if message.content_type in types:
            if text and await check_hidden_links(chat_id, message):
                status, n = await check_filter(chat_id, text)
                if status:
                    await asyncio.sleep(n)
                    await bot.delete_message(chat_id, message.message_id)
            else:
                await bot.delete_message(chat_id, message.message_id)
    else:
        pass
        #await bot.delete_message(chat_id, message.message_id)