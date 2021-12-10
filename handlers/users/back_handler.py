import asyncio
from aiogram.types.message import Message

from aiogram import bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.storage import DisabledStorage
from aiogram.types import ReplyKeyboardRemove , InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from keyboards.default.skip_date_keyboard import skip_button
from keyboards.default.back import back

from loader import db, dp



@dp.message_handler(text="🔙 ortga", state="*")
async def clean_db(message:Message, state: FSMContext):
    await state.finish()
    await message.delete()
    data = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await data.delete() 