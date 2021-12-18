import asyncio
import logging
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from datetime import datetime
from keyboards.default.back import back
from keyboards.default.main_menu import main_button
from loader import db, dp, bot 
from data.config import ADMINS



@dp.message_handler(text="☎️Aloqa (Admin bilan)")
async def pre_contact(message: Message, state: FSMContext):
    await message.answer(f"Yaxshi, savol va takliflaringizni <a href='https://t.me/RRE_MRX'>Adminga </a> yo'llashingiz mumkin",reply_markup=main_button, disable_web_page_preview=True)


