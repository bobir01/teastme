import asyncio
import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.text_decorations import HtmlDecoration
from keyboards.inline.subscribe_keyboard import check_button

from data.config import CHANNELS
from utils.misc.subscription import check
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return
        logging.info(user)
        result = "Iltimos botimizdan foydalanish uchun kanalimizga az'o bo'ling !\n"
        final_status = True
        for channel in CHANNELS:
            status = await check(user_id=user, channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                result += (f"👉 <a href='{invite_link}'>{channel.title}</a>\n")

        if not final_status:
            if update.message:
                await update.message.answer(result, reply_markup=check_button , disable_web_page_preview=True)
                raise CancelHandler()
            else:
                await update.callback_query.answer(f"{channel.title} Kanalimizga az'o bo'lmagansiz", show_alert=True)
                logging.info(update.callback_query)
                raise CancelHandler()
        