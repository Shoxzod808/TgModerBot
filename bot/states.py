from aiogram.dispatcher.filters.state import StatesGroup, State

class New_chanel(StatesGroup):
    info = State()

class Edit_white_list(StatesGroup):
    data = State()

class Edit_black_list(StatesGroup):
    data = State()
