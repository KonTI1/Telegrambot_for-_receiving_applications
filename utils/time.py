from datetime import datetime, date
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sheets.table import get_appointments_for_date

def generate_time_keyboard(selected_date: date) -> InlineKeyboardMarkup:
    all_slots = ["10:00", "12:00", "14:00", "16:00", "18:00"]
    now = datetime.now()

    if selected_date == now.date():
        current_hour = now.hour
        all_slots = [slot for slot in all_slots if int(slot.split(":")[0]) > current_hour]

    busy_slots = get_appointments_for_date(selected_date.strftime("%d.%m.%Y"))
    available_slots = [slot for slot in all_slots if slot not in busy_slots]

    buttons = [
        InlineKeyboardButton(text=slot, callback_data=f"time:{selected_date}|{slot}")
        for slot in available_slots
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    )
    return keyboard
