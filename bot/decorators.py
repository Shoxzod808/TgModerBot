from typing import get_origin
from aiogram.types import Message
from asgiref.sync import sync_to_async
import contextlib

import config
from backend.models import BotUser, Template, Template2Button, Group


def print_msg(func, text):
    print(f'from modul decorators({func}) -> ', text)



@sync_to_async
def add_user(message: Message) -> None:
    chat_id = message.from_user.id
    user, success = BotUser.objects.get_or_create(chat_id=chat_id)
    if success:
        full_name = ' '.join([message.from_user.first_name, message.from_user.last_name or ''])
        user.full_name = full_name
        with contextlib.suppress(Exception):
            user.username = message.from_user.username
        user.save()

@sync_to_async
def is_bot(message: Message) -> bool:
    return message.from_user.is_bot

@sync_to_async
def exists(chat_id) -> bool: 
    return BotUser.objects.filter(chat_id=chat_id).exists()

@sync_to_async
def get_text(title, chat_id, button=False):
    if button:
        text = Template2Button.objects.get(title=title)
    else:
        text = Template.objects.get(title=title)
    lang = BotUser.objects.get(chat_id=chat_id).language
    return text.body_ru if lang == 'ru' else text.body_eng

@sync_to_async
def get_user_lang(chat_id):
    user = BotUser.objects.get(chat_id=chat_id)
    return user.language

@sync_to_async
def set_user_language(chat_id, lang):
    user = BotUser.objects.get(chat_id=chat_id)
    user.language = lang
    user.save()

@sync_to_async
def create_group(title, username, link, description, members_count, chat_id, chanel_chat_id, type):
    user = BotUser.objects.get(chat_id=chat_id)
    return Group.objects.create(
        chat_id=chanel_chat_id,
        title=title,
        username=username, 
        link=link, 
        description=description, 
        users_count=members_count, 
        black_list='-', 
        white_list='-', 
        user=user, 
        type=type
        )

@sync_to_async
def get_list_chats(chat_id) -> list:
    buttons = []
    user = BotUser.objects.filter(chat_id=chat_id)
    if user.exists():
        user = user[0]
        buttons.extend(list(Group.objects.filter(user=user)))
    return buttons

@sync_to_async
def get_group(id):
    return Group.objects.get(id=id)