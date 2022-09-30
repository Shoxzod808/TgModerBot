from aiogram.types import Message
from aiogram import Bot
from bot.config import CHAT_ID


import decorators
import functions

#TopMuzicBot
async def start_command(bot: Bot, message: Message):
    if not await decorators.is_bot(message):
        chat_id = message.from_user.id
        if await decorators.exists(chat_id):
            if 'new' in message.text:
                group_chat_id = message.chat.id
                member = await bot.get_chat_member(group_chat_id, CHAT_ID)
                chat = await bot.get_chat(group_chat_id)
                if member.is_chat_member():
                    if member.status == 'member':
                        text = await decorators.get_text(title='member2group', chat_id=chat_id)
                        keys = chat.iter_keys()
                        await decorators.create_group(
                            title=chat.title,
                            username='-' if 'username' not in keys else chat.username,
                            link='-' if 'username' not in keys else f'https://t.me/{chat.username}',
                            description='-' if 'description' not in keys else f'https://t.me/{chat.description}',
                            members_count=await bot.get_chat_members_count(group_chat_id),
                            chat_id=chat_id,
                            chanel_chat_id=group_chat_id,
                            type='Chat'
                        )

                        await bot.send_message(chat_id, text)
                        text = await functions.get_chanel_info(
                            title=chat.title,
                            username='-' if 'username' not in keys else chat.username,
                            link='-' if 'username' not in keys else f'https://t.me/{chat.username}',
                            description='-' if 'description' not in keys else f'https://t.me/{chat.description}',
                            members_count=await bot.get_chat_members_count(group_chat_id),
                            chat_id=chat_id
                        )
                        await bot.send_message(chat_id, text)
                    elif member.status == 'administrator':
                        text = await decorators.get_text(title='admin2group', chat_id=chat_id)
                        keys = chat.iter_keys()
                        await decorators.create_group(
                            title=chat.title,
                            username='-' if 'username' not in keys else chat.username,
                            link='-' if 'username' not in keys else f'https://t.me/{chat.username}',
                            description='-' if 'description' not in keys else f'https://t.me/{chat.description}',
                            members_count=await bot.get_chat_members_count(group_chat_id),
                            chat_id=chat_id,
                            chanel_chat_id=group_chat_id,
                            type='Chat'
                        )
                        await bot.send_message(chat_id, text)
                        text = await functions.get_chanel_info(
                            title=chat.title,
                            username='-' if 'username' not in keys else chat.username,
                            link='-' if 'username' not in keys else f'https://t.me/{chat.username}',
                            description='-' if 'description' not in keys else f'https://t.me/{chat.description}',
                            members_count=await bot.get_chat_members_count(group_chat_id),
                            chat_id=chat_id
                        )
                        await bot.send_message(chat_id, text)
            else:
                if message.chat.id == chat_id:
                    await functions.send_menu(bot, chat_id)
        else:
            await decorators.add_user(message)
            await functions.send_language_post(bot, chat_id)
            