import html

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from core.States import States
from keyboard.keyboards import start_menu as kb
from utils.data import generate_date_keyboard as data_kb
from core.config import Settings
from filters.check_phone import is_valid_phone

router = Router()
settings = Settings()

async def start_handler(message: Message, state: FSMContext):
    await state.set_state(States.waiting_service)
    await message.answer(f"Добрый день <b>{html.escape(message.from_user.first_name)}</b>! Оставьте заявку", 
                         reply_markup=kb)

async def name_handler(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(States.waiting_phone)
    await message.answer("Введите номер телефона:\n\nВ формате +7ХХХХХХХХХХ")

async def phone_handler(message: Message, state: FSMContext):
    phone = message.text
    if not is_valid_phone(phone):
        await message.answer("Некорректный номер телефона. Повторите ввод.")
        return
    await state.update_data(phone = message.text)
    await state.set_state(States.waiting_date)
    await message.answer("Выберите дату:", reply_markup=data_kb())
def register_handlers():
    router.message.register(start_handler, CommandStart())
    router.message.register(name_handler, States.waiting_name)
    router.message.register(phone_handler, States.waiting_phone)
    