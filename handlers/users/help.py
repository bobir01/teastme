import asyncio
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from aiograph import Telegraph, exceptions
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiograph.utils.exceptions import TelegraphError
from keyboards.default.main_menu import main_button
from loader import dp, db
import logging
from datetime import datetime  
 

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam\n",
            "<b>🧑‍💻Test yaratish</b>(faqat adminlar uchun) \
bu orqali siz o'z auditoriyangizdan test olishingiz, reytinglashingiz \
va g'oliblarni taqdirlashingiz mumkin \n\n<b>✅Test topshirish </b>orqali testlarda qatnashishingiz va o'z natijangizni aniqlab olishingiz\
 mumkin va albatta test yakunida sertifikatga ega bo'lasiz!\n\n \
<b>ℹ️Mening testlarim</b>(adminlar uchun) orqali siz yaratgan testlaringiz haqida to'liqroq ma'lumot olasiz\n\n \
<b>📈Mening natijalarim</b>orqali siz o'z bilim olish darajangizni nazorat qilib borsangiz bo'ladi bot \
sizga qanday natija va yutuqlarga erishganingizni ko'rsatadi\n \
<b>🔄Ismni yangilash </b>bu orqali siz test topshirishdagi ismingizni belgilashingiz mumkin \
botimizdan foydalanishni boshlashingizdanoq ismingiz telegram ismingiz kabi qayt etiladi \
\
Dasturchilar bilan bog'lanish uchun @Bobir_Mardonov @Sabirbaev_Amir")
    
    await message.answer("\n".join(text))
    



@dp.message_handler(text="📈Mening natijalarim")
async def resilts_participated(message: types.Message):
    # logging.info(message)
    datas = await db.participated_tests(user_id=message.from_user.id)
    # logging.info(datas)
    my_tests = "Siz qatnashgan testlar bo'yicha jami ma'lumot<br>"
    counter = 0
    for data in datas:
        my_tests+=f" {data[0]}: "
        my_tests+=f"Test raqami: {data[1]}<br>"
        my_tests+=f"Javoblar: {data[2]}<br>"
        my_tests+=f"Natija: {data[3]} to'g'ri javob <br>"
        my_tests+=f"Topshirilgan : {data[4].strftime('%y-%m-%d %H:%M')}<br><br>"
        counter +=1
    my_tests +=f"<b>Jami qatnashilgan testlar soni</b>: {counter}"
    # await message.answer(my_tests, reply_markup=main_button)
    loop = asyncio.get_event_loop()
    telegraph = Telegraph()
    async def create_page(mytest):
        # loop = asyncio.get_event_loop() 
        await telegraph.create_account('Bobir_Mardonov')
        page = await telegraph.create_page(title=f"Siz qatnashgan barcha testlar ",content=f"<p><strong> {mytest} </strong></p>")
        print('Created page:', page.url)
        return page.url
    
    try:

        page = await create_page(my_tests)
    except TelegraphError as err :
        pass 
        print(err)
    finally:
        # await telegraph.close()
        await telegraph.close()
   
    result_button = InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                InlineKeyboardButton(text="Testlani ko'rish 🚀", url=f"{page}")
                                ],
                            ])
    
    # await message.answer(f"Barcha qatnashilgan testlar {counter}",reply_markup=result_button)
                        
    await message.answer(f"Barcha qatnashilgan testlar {counter}",reply_markup=result_button)