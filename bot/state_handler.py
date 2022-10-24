from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot.functions import black_list
from config import CHAT_ID
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
            member = await bot.get_chat_member(chanel_chat_id, CHAT_ID)
            if not member.is_chat_admin():
                raise RuntimeError
            chanel = await bot.get_chat(chanel_chat_id)
            keys = list(chanel.iter_keys())
            info = {
                'title':'',
                'username': '-',
                'link': '-',
                'description': '-',
                'members_count': 0
            }
            if 'title' in keys:
                info['title'] = chanel.title
            if 'username' in keys:
                info['username'] = f'@{chanel.username}'
                info['link'] = f' https://t.me/{chanel.username}'
            if 'description' in keys:
                info['description'] = chanel.description
            info['members_count'] = await bot.get_chat_members_count(chanel_chat_id)
            text = await decorators.get_text(title='chaneladded', chat_id=chat_id)
            await bot.send_message(chat_id, text, disable_web_page_preview=True)
            text = await functions.get_chanel_info(
                title=info['title'],
                username=info['username'],
                link=info['link'],
                description=info['description'],
                members_count=info['members_count'],
                chat_id=chat_id
            )

            await bot.send_message(chat_id, text, disable_web_page_preview=True)
            await decorators.create_group(
                title=info['title'],
                username=info['username'],
                link=info['link'],
                description=info['description'],
                members_count=info['members_count'],
                chat_id=chat_id,
                chanel_chat_id=chanel_chat_id,
                type='Chanel'
            )
            """async with state.proxy() as data:
                data['info'] = info """
            
            await state.finish()
        
        except Exception as e:
            await print_msg('test_handler1', e)
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
    

async def edit_white_list(bot: Bot, message: Message, state: FSMContext):
    chat_id = message.from_user.id
    group_id = await decorators.get_user_group_id_state(chat_id)
    text = message.text
    try:
        if text == '/empty':
            await decorators.set_group_white_or_black_list(group_id, 'white', '-')
        else:
            await decorators.set_group_white_or_black_list(group_id, 'white', text)
    except Exception as e:
        print('STATE EX PRINT(E)', e)
    finally:
        keyboard = InlineKeyboardMarkup()
        text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
        keyboard.add(InlineKeyboardButton(text2button, callback_data=f'White list-{group_id}'))
        text = await decorators.get_text('data edited', chat_id)
        await bot.send_message(chat_id, text, reply_markup=keyboard)
        await state.finish()

async def edit_black_list(bot: Bot, message: Message, state: FSMContext):
    chat_id = message.from_user.id
    group_id = await decorators.get_user_group_id_state(chat_id)
    text = message.text
    try:
        if text == '/empty':
            await decorators.set_group_white_or_black_list(group_id, 'black', '-')
        else:
            await decorators.set_group_white_or_black_list(group_id, 'black', text)
    except Exception as e:
        print('STATE EX PRINT(E)', e)
    finally:
        keyboard = InlineKeyboardMarkup()
        text2button = await decorators.get_text(title='back', chat_id=chat_id, button=True)
        keyboard.add(InlineKeyboardButton(text2button, callback_data=f'Black list-{group_id}'))
        text = await decorators.get_text('data edited', chat_id)
        await bot.send_message(chat_id, text, reply_markup=keyboard)
        await state.finish()