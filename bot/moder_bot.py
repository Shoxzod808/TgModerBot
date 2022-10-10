from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ContentType, ParseMode
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import New_chanel, Edit_white_list, Edit_black_list
from filter import handler, chanel_handler

import config
from commands import start_command
from handlers import callback_query
from state_handler import test_handler, edit_white_list, edit_black_list

storage = MemoryStorage()
bot = Bot(token=config.TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)



scheduler = AsyncIOScheduler()

async def f():
    print('21qewds')

def get_horoscope_everyday() -> None:
    scheduler.add_job(f, "interval", seconds=2)


async def on_startup(_):
    print('Бот запущен')
    #get_horoscope_everyday()

async def on_shutdown(_):
    print('Бот отключён', end=' ')



@dp.callback_query_handler(lambda call:True)
async def callback_query_handler(call):
    await callback_query(bot, call)
    
@dp.message_handler(Command('start'))
async def start_message_handler(message):
    await start_command(bot, message)



@dp.channel_post_handler(content_types=ContentType.all())
async def channel_handler(message):
    await chanel_handler(bot, message)

@dp.message_handler(content_types=ContentType.all())
async def text_message_handler(message):
    await handler(bot, message)



@dp.message_handler(content_types=ContentType.all(), state=New_chanel.info)
async def test_message_handler(message: Message, state: FSMContext):
    await test_handler(bot, message, state)


@dp.message_handler(content_types=ContentType.TEXT, state=Edit_white_list.data)
async def white_list_message_handler(message: Message, state: FSMContext):
    await edit_white_list(bot, message, state)

@dp.message_handler(content_types=ContentType.TEXT, state=Edit_black_list.data)
async def black_list_message_handler(message: Message, state: FSMContext):
    await edit_black_list(bot, message, state)

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

