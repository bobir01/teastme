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
            KeyboardButton(text="🔄Ismni yangilash"),
            KeyboardButton(text="Sertifikat")
        ]
    ],resize_keyboard=True
)