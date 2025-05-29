from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from core.States import States
from keyboard.keyboards import services as kb
from keyboard.keyboards import help
from utils.time import generate_time_keyboard
from sheets.table import save_appointment
from core.config import Settings

router = Router()
setting = Settings()

async def select_service(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите услугу", reply_markup=kb)

async def remont_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(service = "ремонт")
    await state.set_state(States.waiting_name)
    await callback.message.answer("Введите ваше имя:")
    
async def manic_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(service = "маникюр")
    await state.set_state(States.waiting_name)
    await callback.message.answer("Введите ваше имя:")
    
async def poshiv_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(service = "пошив")
    await state.set_state(States.waiting_name)
    await callback.message.answer("Введите ваше имя:")
    
async def install_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(service = "установка")
    await state.set_state(States.waiting_name)
    await callback.message.answer("Введите ваше имя:")

async def process_date_callback(callback: CallbackQuery, state: FSMContext):
    # Получаем строку даты
    date_str = callback.data.split(":")[1]  # "2025-05-29"
    selected_date = datetime.fromisoformat(date_str).date()
    await state.update_data(date=selected_date.strftime("%d.%m.%Y"))
    await callback.answer(f"Вы выбрали: {selected_date.strftime('%d.%m.%Y')}")
    await state.set_state(States.waiting_time)
    # Теперь отправим клавиатуру со слотами времени
    time_keyboard = generate_time_keyboard(selected_date)
    await callback.message.edit_text(
        f"Выберите время для {selected_date.strftime('%d.%m.%Y')}:",
        reply_markup=time_keyboard
    )

async def process_time_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split(":", 1)[1]  # после первого ":"
    date_str, time_str = data.split("|")
    time_str = time_str.replace("-", ":")  # заменяем "-" обратно в ":"
    await state.update_data(time=time_str)
    data = await state.get_data()
    save_appointment(
        callback.from_user.id,
        data["name"],
        data["phone"],
        data["service"],
        data["date"],
        data["time"]
    )
    await state.clear()
    await callback.bot.send_message(setting.ADMIN_ID[0], f"Новая заявка:\n"
                                    f"Имя: {data['name']}\n"
                                    f"Номер телефона: {data['phone']}\n"
                                    f"Услуга: {data['service']}\n"
                                    f"Дата: {data['date']}\n"
                                    f"Время: {data['time']}")
    
    await callback.message.answer(f'Спасибо за заявку, с вами свяжутся!'
                                  f'\nУслуга: {data["service"]}'
                                  f"\nДата: {date_str}"
                                  f"\nВремя: {time_str}"
                                  f"\nНомер телефона: {data['phone']}"
                                  f"\nВсего доброго!")

async def help_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Помощь")
    
def register_handlers():
    router.callback_query.register(select_service, F.data == "service")
    router.callback_query.register(remont_handler, F.data == "remont")
    router.callback_query.register(manic_handler, F.data == "manic")
    router.callback_query.register(poshiv_handler, F.data == "poshiv")
    router.callback_query.register(install_handler, F.data == "install")
    router.callback_query.register(process_date_callback, F.data.startswith("date:"))
    router.callback_query.register(process_time_callback, F.data.startswith("time:"))
    router.callback_query.register(help_handler, F.data == "help")