from aiogram.filters.state import StatesGroup, State


class States(StatesGroup):
    waiting_service = State()
    waiting_name = State()
    waiting_phone = State()
    waiting_date = State()
    waiting_time = State()
    waiting_confirmation = State()