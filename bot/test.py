from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from states import Test

from config import TOKEN

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


button = InlineKeyboardMarkup(row_width=1)
button.add(InlineKeyboardButton(text='Test', callback_data='test'))

@dp.callback_query_handler(text='test')
async def test_callback_query_handler(call: CallbackQuery):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    text = 'Пришлите мне текст который хотите сохранить.'
    
    await Test.chat_id.set()
    await bot.edit_message_text(text, chat_id, message_id)




@dp.message_handler(content_types=ContentType.TEXT, state=Test.chat_id)
async def test_message_handler(message: Message, state: FSMContext):
    chat_id = message.from_user.id

    async with state.proxy() as data:
        data['chat_id'] = chat_id

    await message.reply('asdasdas')
    await Test.next()




@dp.message_handler(content_types=ContentType.TEXT, state=Test.name)
async def name_message_handler(message: Message, state: FSMContext):
    chat_id = message.from_user.id

    async with state.proxy() as data:
        data['name'] = message.from_user.first_name 

    
    data = await state.get_data()
    user_id = data['chat_id']
    name = data['name']
    await state.finish()
    text = ''
    text += user_id + ' ' + name
    await bot.send_message(chat_id, text)



@dp.message_handler(commands='start')
async def start_command_handler(message: Message):
    chat_id = message.from_user.id
    text = 'Привет'
    await bot.send_message(chat_id, text, reply_markup=button)



if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)