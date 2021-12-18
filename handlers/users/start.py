import asyncio
from aiogram.dispatcher.storage import FSMContext

from aiogram.types.reply_keyboard import ReplyKeyboardRemove
import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from datetime import datetime
from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from keyboards.inline.subscribe_keyboard import check_button
from keyboards.default.main_menu import main_button
from utils.misc.subscription import check
import logging


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    
    if message.is_command():
        await asyncio.sleep(0.1)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                full_name=message.from_user.full_name,
                                username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    # await message.answer(f"Xush kelibsiz! {message.from_user.full_name}", reply_markup=ReplyKeyboardRemove())

    # ADMINGA xabar beramiz
    count = await db.count_users()
    tg_user = message.from_user.get_mention(as_html=True)
    msg = f"{tg_user} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)
    # await state.set_state("start_finish")
    await state.finish()
    logging.info(message.message_id)
    for channel in CHANNELS:
        status = await check(user_id=message.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            a = await message.answer(f"@botlinki - bu sizning \
yordamchingiz 😊.\n\nSiz bot yordamida o'z auditoriyangizdan \
testlar olishingiz mumkin. \n\nFoydalanish bo'yicha to'liq ma'lumot olish uchun /help buyrug'idan foydalaning", reply_markup=main_button)
            
            
            
           
        else:
            result = (f"Iltimos botimizdan foydalanish uchun kanalimizga az'o bo'ling !:\n")
            await message.answer(result, reply_markup=check_button, disable_web_page_preview=True)
    
    await state.finish()

@dp.callback_query_handler(text="check_subs", state="*")
async def checker(call: types.CallbackQuery, state:FSMContext):
    # await call.answer(f" Kanalimizga az'o bo'lmagansiz", show_alert=True)    

    for channel in CHANNELS:
        status = await check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            await call.answer("Bajarildi") 
            await call.message.answer(f"@botlinki - bu sizning yordamchingiz 😊.\n\nSiz bot yordamida o'z \
auditoriyangizdan testlar olishingiz mumkin. \n\nFoydalanish bo'yicha to'liq ma'lumot olish uchun /help buyrug'idan foydalaning", reply_markup=main_button)
            
            await bot.delete_message(chat_id=call.from_user.id,message_id=call.message.message_id)
        else:
            result = (f"⛔️Iltimos botimizdan foydalanish uchun kanalimizga az'o bo'ling !:\n")
            a = await call.message.answer(result, reply_markup=check_button, disable_web_page_preview=True)
            await asyncio.sleep(15)
            await a.delete()
   