from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Выбор услуги', callback_data='service'),
            InlineKeyboardButton(text='Помощь', callback_data='help')
        ],
    ]
)

services = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ремонт', callback_data='remont'),
            InlineKeyboardButton(text='маникюр', callback_data='manic'),
        ],
        [
            InlineKeyboardButton(text='пошив', callback_data='poshiv'),
            InlineKeyboardButton(text='установка', callback_data='install'),
        ],
    ]
)

help = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Помощь', callback_data='help'),
        ],
    ]
)