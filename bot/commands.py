from aiogram.types import Message
from aiogram import Bot
from bot.decorators import is_bot


import decorators
import functions

#TopMuzicBot
async def start_command(bot: Bot, message: Message):
    if not await decorators.is_bot(message):
        chat_id = message.from_user.id
        if not await decorators.exists(chat_id):
            await decorators.add_user(message)
            await functions.send_language_post(bot, chat_id)
        else:
            await functions.send_menu(bot, chat_id)