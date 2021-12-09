from aiogram.dispatcher.storage import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from datetime import datetime
from loader import dp, db, bot
from data.config import ADMINS


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
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
    await state.finish()
    
    my_test = await db.select_test_with_results(owner_id=message.from_user.id, test_number=int(15))
    print("if dan oldin")
    if my_test:
        print("if ga kirdi ")
        results = ""
        for n in my_test:
            # results +=f" Test raqamai  {n[0]}\n"
            # results +=f" Test nomi   {n[1]}\n"
            # results +=f" Test raqamai  {n[2]}\n"
            # results +=f" Test javobi  {n[3]}\n"
            # results +=f" Boshlanish vaqti  {n[4]}\n"
            # results +=f" Tugash vaqti   {n[5]}\n"
            pass
        full_info = f" Test raqami {my_test[0]}\n Test nomi   {my_test[1]}\n Test javobi  {my_test[2]}\n Boshlanish vaqti  {my_test[3]}\n Tugash vaqti   {my_test[4]}\n"
        print(full_info)
    else:
        print("else pronlem")