import asyncio
import logging
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from datetime import datetime
from keyboards.default.back import back
from keyboards.default.main_menu import main_button
from loader import db, dp



dp.message_handler(text="📈Mening natijalarim")
async def participated_tests(message:Message):
    logging.info(message)
    datas = await db.participated_tests(user_id=message.from_user.id)
    logging.info(datas)
    my_tests = "Siz qatnashgan testlar bo'yicha jami ma'lumot"
    counter = 0
    for data in datas:
        my_tests+=f" {data[0]}"
        my_tests+=f"Test raqami: {data[1]}\n"
        my_tests+=f"Javoblar: {data[2]}\n"
        my_tests+=f"Natija: {data[3]}\n"
        my_tests+=f"Topshirilgan : {data[4]}\n"
        counter +=1
    my_tests +=f"<b>Barcha qatnashilgan testlar soni</b> : {counter}"
    await message.answer(my_tests, reply_markup=main_button)