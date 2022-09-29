from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import Bot


from states import Test

async def test_handler(bot: Bot, message: Message, state: FSMContext):
    chat_id = message.from_user.id
    async with state.proxy() as data:
        data['chat_id'] = chat_id

    await message.reply('asdasdas')
    await Test.next()


async def name_handler(bot: Bot, message: Message, state: FSMContext):
    chat_id = message.from_user.id

    async with state.proxy() as data:
        data['name'] = message.from_user.first_name 

  
    data = await state.get_data()
    user_id = data['chat_id']
    name = data['name']
    await state.finish()
    text = ''
    text += str(user_id) + ' ' + name
    await bot.send_message(chat_id, text)