from functools import partial
from typing import Dict
from aiogram import executor
from datetime import datetime

from loader import dp, db
import middlewares, filters, handlers
from utils.db_api import tests
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_users()
    await db.create_table_users()
    await db.create_test_table()
    await db.create_test_config()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


    
    now = datetime.now()
    
    config = await db.select_test_config(1)
    partis = await db.count_participants_via_test(1) # retrun totals participants of test

    
    dashboard = await db.select_dashboard(1)
  
    text = ""
    for x in dashboard:
        text +=f"{x[0]}. "
        text +=f" Ism sharifi  {x[1]}"
        text +=f"     javoblari:  {x[2]}"
        text +=f"     natija:  {x[3]}\n"
    print(text)
        
       




if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
