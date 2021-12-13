from aiogram.dispatcher.storage import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from datetime import datetime
from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from keyboards.inline.subscribe_keyboard import check_button


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
#     for channel in CHANNELS:
#         status = await subscription.check(user_id=message.from_user.id, channel=channel)
#         channel = await bot.get_chat(channel)
#         if status:
#             await message.answer(f"@botlinki - bu sizning \
# yordamchingiz 😊.\n\nSiz bot yordamida o'z auditoriyangizdan \
# testlar olishingiz mumkin. \n\nFoydalanish bo'yicha to'liq ma'lumot olish uchun /yordam buyrug'idan foydalaning")
#         else:
#             result = (f"Iltimos botimizdan foydalanish uchun kanalimizga az'o bo'ling !:\n")
#             await message.answer(result, reply_markup=check_button, disable_web_page_preview=True)
    

    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                full_name=message.from_user.full_name,
                                username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    await message.answer(f"Xush kelibsiz! {message.from_user.full_name}", reply_markup=ReplyKeyboardRemove())

    # ADMINGA xabar beramiz
    count = await db.count_users()
    msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)
    # await state.set_state("start_finish")
    await state.finish()



# @dp.callback_query_handler(text="check_subs", state="*")
# async def checker(call: types.CallbackQuery):
#     await call.answer()
#     for channel in CHANNELS:
#         status = await subscription.check(user_id=call.from_user.id, channel=channel)
#         channel = await bot.get_chat(channel)
#         if status:
#             await call.message.answer(f"@botlinki - bu sizning yordamchingiz 😊.\n\nSiz bot yordamida o'z auditoriyangizdan testlar olishingiz mumkin. \n\nFoydalanish bo'yicha to'liq ma'lumot olish uchun /yordam buyrug'idan foydalaning")
#         else:
#             result = (f"⛔️Iltimos botimizdan foydalanish uchun kanalimizga az'o bo'ling !:\n")
#             await call.message.answer(result, reply_markup=check_button, disable_web_page_preview=True)