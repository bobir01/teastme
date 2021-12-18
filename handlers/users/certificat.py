import asyncio
import os 
from os import path
from aiogram.types import InputFile
from aiograph import Telegraph
from aiogram.types.message import Message
# from telegraph import Telegraph 
from aiogram import bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.storage import DisabledStorage
from aiogram.types import ReplyKeyboardRemove , InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from keyboards.default.skip_date_keyboard import skip_button
from keyboards.default.back import back
from keyboards.default.main_menu import main_button
from utils.certificate_make import certify
from loader import db, dp



@dp.message_handler(text="Sertifikat")
async def certificat(message:Message, state: FSMContext):
    await message.answer("Yaxshi qatnashgan testingiz raqamini yuboring:", reply_markup=back)
    await state.set_state("test_num_certificat")


@dp.message_handler(state="test_num_certificat")
async def certificat(message:Message, state: FSMContext):
    test_num = message.text
    if test_num == "🔙 ortga":
        await state.finish()
        
    if test_num.isdigit():
        score = await db.data_for_certi(user_id=message.from_user.id, test_number=int(test_num))
        if score: 
            photo_file = certify(name=message.from_user.full_name, score=score[0][0], user_id=message.from_user.id)
            photo = InputFile(path_or_bytesio=f"./res_certificats/{message.from_user.id}_result.jpg")
            await message.answer_photo(photo=photo)
            await state.finish()
            path = os.path.join(photo_file)
            await asyncio.sleep(10)
            os.remove(path)
        else:
            await message.answer("Bu testda siz qatnashmagansiz, Iltimos yana urinib ko'ring!")

    else:
        await message.answer("Iltimos faqat sonlardan foydalaning!")


