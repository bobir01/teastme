import asyncio
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
from data.config import ADMINS
from loader import db, dp



@dp.message_handler(Command("clean"), state="*")
async def clean_db(message:Message):
    await db.delete_test_table()
    await db.delete_config()
    await db.delete_users()
    await message.answer("cleaned")


# to collect all messages of user in one message with state 
@dp.message_handler(text="🧑‍💻Test yaratish", state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
            
        await message.answer("Demak yangi test qo'shmoqchisiz, yaxshi, testni qanday nomlaymiz ?", reply_markup=back)
        await state.set_state("test_name")
    else:
        await message.answer("Afsus siz test yarata olmaysiz. Faqat adminlar test yaratishadi", reply_markup=back)
        await state.finish()
@dp.message_handler(state="test_name")
async def bot_start(message: types.Message, state: FSMContext):
    test = message.text
    if test == "🔙 ortga":
        
        await message.answer("Yaxshi siz test yaratishni bekor qildingiz")
    else:
            
        await state.update_data({
            "test_name" : test
        })

        x = datetime.now()

        day = x.strftime("%d")
        month = x.strftime("%m")
        year = x.strftime("%Y")
        hours = x.strftime("%H")
        minute = x.strftime("%M")

        
        await message.answer(f"Yaxshi, ushbu test qachon \
boshlanadi ?\n\nVaqtni <b>KK.OO.YYYY SS:MM </b>ko'rinishida kiriting,\
bunda\n\nYYYY - yil\nKK - kun\nOO - Oy\n\nSS - soat\nMM - minut\n\nMasalan: {day}.{month}.{year} {hours}:{minute}", reply_markup=skip_button)
        
        await state.set_state("time")


@dp.message_handler(state="time")
async def bot_start(message: types.Message, state: FSMContext):
    test = message.text
    if test == "🔙 ortga":
        state.finish()
        await message.answer("Yaxshi siz test yaratishni bekor qildingiz")
    else:
        x = datetime.now()
        day = x.strftime("%d")
        month = x.strftime("%m")
        year = x.strftime("%Y")
        hours = x.strftime("%H")
        minute = x.strftime("%M")
        if test != "skip":        
            

            try:

                year1 = test[6:10]
                month1 =test[3:5]
                day1 = test[:2]
                hour1 = test[11:13]
                minute1 = test[14:16]
                s_date = datetime(int(year1), int(month1) ,int(day1) ,int(hour1) ,int(minute1))
                if x < s_date:
                    await state.update_data({
                        "start_time" : test
                    })
                    await state.set_state("end_time")
                    await message.answer(f"Boshlanish vaqti saqlandi,\
qachon yakunlanadi ?\nVaqtni <b>KK.OO.YYYY SS:MM </b>ko'rinishida\
kiriting, bunda\n\nYYYY - yil\nKK - kun\nOO - Oy\n\nSS - soat\n\nMM -\
minut\nMasalan: {day}.{month}.{year} {hours}:{minute}", reply_markup=skip_button)
                else:
                    await message.answer("O'tib ketgan vaqtda testni boshlay olmayman boshqa sana kiritib ko'ring")
            except:
                await message.answer("Sana formatini xato kiritdingiz qayta tekshiring!", reply_markup=back)
        else:
            await state.set_state("end_time")
            await message.answer(f"Boshlanish vaqti saqlandi,\
qachon yakunlanadi ?\nVaqtni KK.OO.YYYY SS:MM ko'rinishida\
kiriting, bunda\n\nYYYY - yil\nKK - kun\nOO - Oy\n\nSS - soat\n\nMM -\
minut\nMasalan: <b>{day}.{month}.{year} {hours}:{minute}</b>", reply_markup=skip_button)
    
            await state.update_data({
                        "start_time" : test
                    })


@dp.message_handler(state="end_time")
async def bot_start(message: types.Message, state: FSMContext):
    test = message.text
    if test == "🔙 ortga":
        state.finish()
        await message.answer("Yaxshi siz test yaratishni bekor qildingiz")
    else:
        x = datetime.now()
        if test != "skip" :

            day = x.strftime("%d")
            month = x.strftime("%m")
            year = x.strftime("%Y")
            hours = x.strftime("%H")
            minute = x.strftime("%M")
            try:            
                year = test[6:10]
                month =test[3:5]
                day = test[:2]
                hour = test[11:13]
                minute = test[14:16]
                end_date = datetime(int(year), int(month) ,int(day) ,int(hour) ,int(minute))

                if x < end_date : #and end_date>start_date:
                    await state.update_data({
                        "end_time" : test
                    })
                    await message.answer("Sanalar muvaffaqiyatli saqlandi endi javoblarni yuboring \nMasalan: abcdabcd", reply_markup=back)
                    await state.set_state("answers")
                else:
                    await message.answer("Tugashni boshlashdan oldin qilishning ilojin yo'q ", reply_markup=back)
            except:
                await message.answer("Sana formatini xato kiritdingiz qayta tekshiring!", reply_markup=back)
        else:
            await state.set_state("answers")
            await state.update_data({
                        "end_time" : test
                    })
            await message.answer("Sanalar muvaffaqiyatli saqlandi endi javoblarni yuboring \nMasalan: 1a2b3c4d5a", reply_markup=back)




@dp.message_handler(state="answers")
async def bot_start(message: types.Message, state: FSMContext):
    text = message.text
    if text == "🔙 ortga":
        state.finish()
        await message.answer("Yaxshi siz test yaratishni bekor qildingiz")
    else:
        await state.update_data({
            "answers" : text})
        
        data = await state.get_data()
        print(data)
        if data["end_time"] =="skip" and data["start_time"] =="skip":
            await db.add_test(owner_id=message.from_user.id, test_name=data["test_name"], answers=data["answers"])
        elif data["start_time"] != "skip" and data["end_time"] !="skip":
            await db.add_test(owner_id=message.from_user.id, test_name=data["test_name"], answers=data["answers"],start_date=data["start_time"] , end_date=data["end_time"] )
        elif data["end_time"] =="skip":
            await db.add_test(owner_id=message.from_user.id, test_name=data["test_name"], answers=data["answers"], start_date=data["start_time"] )   
        else:

            await db.add_test(owner_id=message.from_user.id, test_name=data["test_name"], answers=data["answers"], end_date=data["end_time"] )
        
        await state.finish()
        # to return current test number from database 
        current_test_number = await db.select_inserted_test_number()
        
        all_info = f"sizning testingiz\n\
#️⃣ Test raqami: <b>{current_test_number}</b>\n\
📌 Test nomi: <i>{data['test_name']}</i>\n\
🟢Boshlanish vaqti - <i>{data['start_time']}</i>\n\n\
🔴Tugash vaqti - <i>{data['end_time']}</i>\n\n\
@current_time_123bot beminnat yordamchingiz!"
        await message.answer(all_info)

        await message.answer(f"sizning testingiz\n\
#️⃣ Test raqami: <b>{current_test_number}</b>\n\
📌 Test nomi: <i>{data['test_name']}</i>\n\
🔐 To'g'ri javoblar: <i>{data['answers']}</i>\n\n\
🟢Boshlanish vaqti - <i>{data['start_time']}</i>\n\n\
🔴Tugash vaqti - <i>{data['end_time']}</i>\n\n\
@current_time_123bot beminnat yordamchingiz!", reply_markup=main_button)


@dp.message_handler(text="ℹ️Mening testlarim")
async def my_tests(message: types.Message, state:FSMContext):
    my_test = await db.select_test_numbers(message.from_user.id)
    my_tests = "test raqami:    test nomi\n"
    if my_test:
            
        for test in my_test:
            my_tests +=f"{test[0]}                   |      {test[1]} \n"
            my_tests +="____________________________\n"
    else:
        await message.answer("siz hali test yaratmadingiz \nyaratish uchun Test yaratish buyrug'ini tanlang")
    
    counts = await db.count_user_tests(message.from_user.id)
    my_tests += f" sizning jami testlariniz soni  {counts}\n\n"
    my_tests += "@current_time_123bot"

    await message.answer(my_tests, reply_markup=ReplyKeyboardRemove())
    await state.set_state("test_results")
    await message.answer("Natijalar bilan ko'rish uchun test raqamini yuboring", reply_markup=back)
   



@dp.message_handler(state="test_results")
async def my_tests(message: types.Message, state:FSMContext):
    
    t_number = message.text
    if t_number.isdigit():
            
        if t_number == "🔙 ortga":
            state.finish()
            await message.answer("Yaxshi siz test topshirishni bekor qildingiz")
        else:
            

            my_test = await db.select_test_with_results(owner_id=message.from_user.id, test_number=int(t_number))
            
            if my_test:
                print("2 if ga kirdi ")
                full_info = f"Test raqami <b>{my_test[0]}</b>\n Test nomi   <b>{my_test[1]}</b>\n Test javobi  <b>{my_test[2]}</b>\n Boshlanish vaqti  \
<b>{my_test[3]}</b>\n Tugash vaqti   {my_test[4]}\n\n Qatnashuvchilar soni: {await db.count_participants_via_test(int(my_test[0]))}"
                dashboard = await db.select_dashboard(int(t_number))
                dashboard_admin = await db.select_dashboard_admin(int(t_number))
                print(dashboard)
                if dashboard:     
                    print("if ga kirish")

                    text = f"{int(t_number)} raqamli test natijalari <br>"
                    for x in dashboard:
                        text +=f"{x[0]}.🏅"
                        text +=f" Ism: <b>{x[1]}</b>"
                        text +=f" Javoblar:  <b>{x[2]}</b>"
                        text +=f" Natija: <b>{x[3]}</b><br>"
                        text +=f" Raqam: <b>{x[4]}</b><br><br>"
                    print("shu yerga keldi")
                    admin = f"{int(t_number)} raqamli test natijalari <br>"
                    for ab in dashboard_admin:
                        admin +=f"{ab[0]}.🏅"
                        admin +=f" Ism: <b>{ab[1]}</b>"
                        admin +=f" Javoblar:  <b>{ab[2]}</b>"
                        admin +=f" Natija: <b>{ab[3]}</b><br><br>"
                        

#======================================telegraph===========================================================================
                    try:                 
                        loop = asyncio.get_event_loop()
                        telegraph = Telegraph()
                        
                        # telegraph = Telegraph()
                        # print(telegraph.create_account(short_name='Bobir_Mardonov', author_name='Bobir Mardonov', author_url="http://t.me/Bobir_Mardonov"))
                        await telegraph.create_account('Bobir_Mardonov')
                        page = await telegraph.create_page(title=f"Qatnashuvchilar reyting testi {my_test[0]} {my_test[1]}",content=f"<p>{text}</p>")
                        page_admin = await telegraph.create_page(title=f"Qatnashuvchilar reyting testi {my_test[0]} {my_test[1]}",content=f"<p>{admin}</p>")
                        print('Created page:', page.url)
                    except:
                        pass
                        print("xato bor")
                    finally:
                        await telegraph.close()
                    
                    result_button = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                            InlineKeyboardButton(text="Natijalarni ko'rish (Admin)🚀", url=f"{page.url}")
                            ],
                        ])

                    result_button_admin = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                            InlineKeyboardButton(text="Natijalarni ko'rish 🚀", url=f"{page_admin.url}")
                            ],
                        ])
                    
                    await message.answer(full_info,reply_markup=result_button)
                    await asyncio.sleep(2)
                    await message.answer(full_info,reply_markup=result_button_admin)
                    await state.finish()
                else:
                    await message.answer("Qatnashchilar topilmadi ")
                    await state.finish()
            else:
                await message.answer(f"{int(t_number)} raqamli test sizga tegishli emas yoki unda hech kim qatnashmagan", reply_markup=back)
            

    
            # await message.answer(f"{t_number} ❌ iltimos faqat sonlardan foydalaning  ", reply_markup=back)
    else:
        await message.answer(f"{t_number} ❌ iltimos faqat sonlardan foydalaning! ", reply_markup=back)




@dp.message_handler(text="🔄Ismni yangilash")
async def update_name_state(message:Message, state:FSMContext):
    await message.answer("Testlarda ismingiz telegram ismingiz orqali ro'yxatga olinadi\
 shuning uchun to'liq ismingiz bilan ro'yxatdan o'tishingizni maslahat beramiz \nIsm familyangizni yuboring: ", reply_markup=back)
    await state.set_state("update_name")

@dp.message_handler(state="update_name")
async def update_name(message: Message, state: FSMContext):
    tetx = message.text
    if tetx == "🔙 ortga":
        state.finish()
        await message.answer(f"Yaxshi, Ism yangilishini bekor qildingiz", reply_markup=main_button)
    else:
        await db.update_user_full_name(tetx, telegram_id=message.from_user.id)
        await message.answer(f"Ism Familyangiz muvaffaqiyatli yangilandi!\n\
hozirgi ismingiz {tetx}", reply_markup=main_button)
        await state.finish()



