from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("add_test", "test yaratish"),
            types.BotCommand("my_tests", "testlarni ko'rish"),
            types.BotCommand("send_answers", "javob yuborish"),
            types.BotCommand("update_name", "ismni yangilash")

        ]
    )
