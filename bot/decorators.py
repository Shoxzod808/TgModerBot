from aiogram.types import Message
from asgiref.sync import sync_to_async
import contextlib
from django.db import models
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
def get_group(id) -> models.Model:
    return Group.objects.get(id=id)

@sync_to_async
def get_group_wlist(id) -> models.Model:
    return Group.objects.get(id=id).white_list

@sync_to_async
def get_group_blist(id) -> models.Model:
    return Group.objects.get(id=id).black_list

@sync_to_async
def set_group_bl_timer(n, id):
    group = Group.objects.get(id=id)
    group.black_list_timer = n
    group.save()

@sync_to_async
def copy_filter(group_id, to_group_id):
    if group_id != to_group_id:
        from_group = Group.objects.get(id=group_id)
        to_group = Group.objects.get(id=to_group_id)
        to_group.black_list = from_group.black_list
        to_group.enable_black_list = from_group.enable_black_list
        to_group.black_list_timer = from_group.black_list_timer
        to_group.white_list = from_group.white_list
        to_group.enable_white_list = from_group.enable_white_list
        to_group.save()

@sync_to_async
def edit_status_white_and_black_lists(group_id, type, data, chat_id):
    group = Group.objects.get(id=group_id)
    text = False
    if '✅' in data:
        if type == 'white':
            group.enable_white_list = False
        else:
            group.enable_black_list = False
    elif type == 'white':
        if group.enable_black_list:
            group.enable_black_list = False
            text = Template.objects.get(title='black_or_white')
            lang = BotUser.objects.get(chat_id=chat_id).language
            text = text.body_ru if lang == 'ru' else text.body_eng
        group.enable_white_list = True
    elif type == 'black':
        if group.enable_white_list:
            group.enable_white_list = False
            text = Template.objects.get(title='black_or_white')
            lang = BotUser.objects.get(chat_id=chat_id).language
            text = text.body_ru if lang == 'ru' else text.body_eng
        group.enable_black_list = True
    group.save()
    return text

@sync_to_async
def edit_group_id2user(chat_id, id):
    user = BotUser.objects.get(chat_id=chat_id)
    user.group_id_state = id
    user.save()

@sync_to_async
def get_user(chat_id) -> models.Model:
    return BotUser.objects.get(chat_id=chat_id)

@sync_to_async
def get_user_group_id_state(chat_id):
    return BotUser.objects.get(chat_id=chat_id).group_id_state

@sync_to_async
def set_group_white_or_black_list(id, lst, text):
    group = Group.objects.get(id=id)
    if lst == 'white':
        group.white_list = text
    else:
        group.black_list = text
    group.save()

