from pyrogram import Client
import asyncio

api_id = 15970544
api_hash = '5f19e794de1bca310ca94ad0d0f0295b'

app = Client("my_account", api_id = api_id, api_hash = api_hash )

from_chat_id = 1639933152
link = -1001733300577
async def send_msg(message):
    async with app:
        username = message.from_user.username
        await app.send_message('me', username)





