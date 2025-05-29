from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

def generate_date_keyboard(days_ahead: int = 7) -> InlineKeyboardMarkup:
    today = datetime.now().date()
    buttons = []

    for i in range(days_ahead):
        date = today + timedelta(days=i)
        text = f"{date.day} {MONTHS_RU[date.month]}"
        callback_data = f"date:{date.isoformat()}"
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons[i:i + 2] for i in range(0, len(buttons), 2)
    ])

    return keyboard
