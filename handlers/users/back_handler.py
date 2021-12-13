from aiogram.types.message import Message

from aiogram.dispatcher import FSMContext
from keyboards.default.main_menu import main_button

from loader import dp



@dp.message_handler(text="🔙 ortga", state="*")
async def clean_db(message:Message, state: FSMContext):
    await state.finish()
    await message.delete()
    data = await message.answer(f"@botlinki - bu sizning \
yordamchingiz 😊.\n\nSiz bot yordamida o'z auditoriyangizdan \
testlar olishingiz mumkin. \n\nFoydalanish bo'yicha to'liq ma'lumot olish uchun /yordam buyrug'idan foydalaning", reply_markup=main_button)
    