from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.default.main_menu import main_button
from loader import dp, db
import logging
from datetime import datetime

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam\n",
            "<b>Test yaratish</b>(faqat adminlar uchun) \
bu orqali siz o'z auditoriyangizdan test olishingiz, reytinglashingiz \
va g'liblarni taqdirlashingiz mumkin \n\n<b>Test topshirish </b>orqali testlarda qatnashishingiz va o'z natijangizni aniqlab olishingiz\
 mumkin va albatta test yakunida sertifikatga ega bo'lasiz!\n\n \
<b>Mening testlarim</b>(adminlar uchun) orqali siz yaratgan testlaringiz haqida to'liqroq ma'lumot olasiz\n\n \
<b>Mening natijalarim </b>orqali siz o'z bilim olish darajangizni nazorat qilib borsangiz bo'ladi bot \
sizga qanday natija va yutuqlarga erishganingizni ko'rsatadi\n")
    
    await message.answer("\n".join(text))
    



@dp.message_handler(text="📈Mening natijalarim")
async def resilts_participated(message: types.Message):
    logging.info(message)
    datas = await db.participated_tests(user_id=message.from_user.id)
    logging.info(datas)
    my_tests = "Siz qatnashgan testlar bo'yicha jami ma'lumot\n"
    counter = 0
    for data in datas:
        my_tests+=f" {data[0]}: \n"
        my_tests+=f"Test raqami: {data[1]}\n"
        my_tests+=f"Javoblar: {data[2]}\n"
        my_tests+=f"Natija: {data[3]}\n"
        my_tests+=f"Topshirilgan : {data[4].strftime('%y-%m-%d %H:%M')}\n"
        counter +=1
    my_tests +=f"<b>Jami qatnashilgan testlar soni</b>: {counter}"
    await message.answer(my_tests, reply_markup=main_button)