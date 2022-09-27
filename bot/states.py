from aiogram.dispatcher.filters.state import StatesGroup, State

class Test(StatesGroup):
    chat_id = State()
    name = State()