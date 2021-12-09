from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


skip_button = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="skip")
    ]
    ],resize_keyboard=True
)