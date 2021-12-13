from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧑‍💻Test yaratish"),
            KeyboardButton(text="✅Test topshirish")
        ],
        [
            KeyboardButton(text="📈Mening natijalarim"),
            KeyboardButton(text="ℹ️Mening testlarim"),           
        ],
        [
            KeyboardButton(text="🔄Ismni yangilash")
        ]
    ],resize_keyboard=True
)