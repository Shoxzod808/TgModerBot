from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

import decorators
import functions

from states import New_chanel



async def print_msg(func, text):
    print(f'from modul state_handler({func}) -> ', text)


async def test_handler(bot: Bot, message: Message, state: FSMContext):
    chat_id = message.from_user.id
    try:
        if message.text == '/stop':
            raise ValueError
        chanel_chat_id = message.forward_from_chat.id
        try:
            chanel = await bot.get_chat(chanel_chat_id)
            await functions.fprint(chanel)
            keys = [i for i in chanel.iter_keys()]
            title = ''
            username = '-'
            link = '-'
            description = '-'
            members_count = 0
            if 'title' in keys:
                title = chanel.title
            if 'username' in keys:
                chanel_username = chanel.username
                link = f'https:/t.me//{chanel_username}'
            if 'description' in keys:
                description = chanel.description
            members_count = await bot.get_chat_members_count(chanel_chat_id)
            text = await decorators.get_chanel_info(
                title=title,
                username=username,
                link=link,
                description=description,
                members_count=members_count,
                chat_id=chat_id
            )
            keyboard = InlineKeyboardMarkup()
            text2button = decorators.get_text('')
            keyboard.add(
                InlineKeyboardButton('')
            )
            
            
            async with state.proxy() as data:
                data['chat_id'] = chat_id
            
            await message.reply('asdasdas')
            await state.finish()
        
        except Exception as e:
            await print_msg('test_handler', e)
            text = await decorators.get_text(title='notadmininchat', chat_id=chat_id)
            await bot.send_message(chat_id, text)
            await functions.add_chanel(bot=bot, chat_id=chat_id)
            await state.finish()
            await New_chanel.info.set()
    except ValueError:
        await state.finish()
        await functions.send_menu(bot=bot, chat_id=chat_id)
    except Exception as e:
        await print_msg('test_handler', e)
        text = await decorators.get_text(title='сhannelnotfound', chat_id=chat_id)
        await bot.send_message(chat_id, text)
        await functions.add_chanel(bot=bot, chat_id=chat_id)
        await state.finish()
        await New_chanel.info.set()
    

    


""" async def name_handler(bot: Bot, message: Message, state: FSMContext):
    chat_id = message.from_user.id

    async with state.proxy() as data:
        data['name'] = message.from_user.first_name 

  
    data = await state.get_data()
    user_id = data['chat_id']
    name = data['name']
    await state.finish()
    text = ''
    text += str(user_id) + ' ' + name
    await bot.send_message(chat_id, text) """