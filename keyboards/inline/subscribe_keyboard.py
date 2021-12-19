from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

check_button = InlineKeyboardMarkup(
    inline_keyboard=[[
    InlineKeyboardButton(text="↗️Obuna bo'lish", url="https://t.me/StepUp_institution")
    ],
    [
        InlineKeyboardButton(text="🔁 Obunani tekshirish", callback_data="check_subs")
    ],

    ]
)

