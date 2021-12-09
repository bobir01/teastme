import asyncio
from aiogram.types.message import Message
from telegraph import Telegraph 
from typing import AnyStr
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.storage import DisabledStorage
from aiogram.types import ReplyKeyboardRemove , InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from keyboards.default.skip_date_keyboard import skip_button




from loader import db, dp



# to collect all messages of user in one message with state 
@dp.message_handler(Command("add_test"))
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Demak yangi test qo'shmoqchisiz, yaxshi, testni qanday nomlaymiz ?", reply_markup=ReplyKeyboardRemove())
    await state.set_state("test_name")


@dp.message_handler(state="test_name")
async def bot_start(message: types.Message, state: FSMContext):
    test = message.text
    await state.update_data({
        "test_name" : test
    })
    test = message.text

    x = datetime.now()

    day = x.strftime("%d")
    month = x.strftime("%m")
    year = x.strftime("%Y")
    hours = x.strftime("%H")
    minute = x.strftime("%M")

    
    await message.answer(f"Yaxshi, ushbu test qachon \
boshlanadi ?\n\nVaqtni KK.OO.YYYY SS:MM ko'rinishida kiriting,\
bunda\n\nYYYY - yil\nKK - kun\nOO - Oy\n\nSS - soat\nMM - minut\n\nMasalan: {day}.{month}.{year} {hours}:{minute}", reply_markup=skip_button)
    
    await state.set_state("time")


@dp.message_handler(state="time")
async def bot_start(message: types.Message, state: FSMContext):
    test = message.text
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
qachon yakunlanadi ?\nVaqtni KK.OO.YYYY SS:MM ko'rinishida\
kiriting, bunda\n\nYYYY - yil\nKK - kun\nOO - Oy\n\nSS - soat\n\nMM -\
minut\nMasalan: {day}.{month}.{year} {hours}:{minute}", reply_markup=skip_button)
            else:
                await message.answer("O'tib ketgan vaqtda testni boshlay olmayman boshqa sana kiritib ko'ring")
        except:
            await message.answer("Sana formatini xato kiritdingiz qayta tekshiring!")
    else:
        await state.set_state("end_time")
        await message.answer(f"Boshlanish vaqti saqlandi,\
qachon yakunlanadi ?\nVaqtni KK.OO.YYYY SS:MM ko'rinishida\
kiriting, bunda\n\nYYYY - yil\nKK - kun\nOO - Oy\n\nSS - soat\n\nMM -\
minut\nMasalan: {day}.{month}.{year} {hours}:{minute}", reply_markup=skip_button)
       
        await state.update_data({
                    "start_time" : test
                })


@dp.message_handler(state="end_time")
async def bot_start(message: types.Message, state: FSMContext):
    test = message.text
    x = datetime.now()
    if test != "skip":

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
            s_date = datetime(int(year), int(month) ,int(day) ,int(hour) ,int(minute))

            data = await state.get_data()
            start = data["start_time"]
            year1 = start[6:10]
            month1 =start[3:5]
            day1 = start[:2]
            hour1 = start[11:13]
            minute1 = start[14:16]

            start_date = datetime(int(year1), int(month1) ,int(day1) ,int(hour1) ,int(minute1))
            
            if x < s_date:
                await state.update_data({
                    "end_time" : test
                })
                await message.answer("Sanalar muvaffaqiyatli saqlandi endi javoblarni yuboring \nMasalan: abcdabcd")
                await state.set_state("answers")
            else:
                await message.answer("Tugashni boshlashdan oldin qila olmayman ")
        except:
            await message.answer("Sana formatini xato kiritdingiz qayta tekshiring!")
    else:
        await state.set_state("answers")
        await state.update_data({
                    "end_time" : test
                })
        await message.answer("Sanalar muvaffaqiyatli saqlandi endi javoblarni yuboring \nMasalan: abcdabcd")




@dp.message_handler(state="answers")
async def bot_start(message: types.Message, state: FSMContext):
    text = message.text
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
    await asyncio.sleep(1)
    current_test_number = await db.select_inserted_test_number()
    print(current_test_number)
    await message.answer(f"sizning testingiz\n\n\
test number - {current_test_number}\n \
test name - {data['test_name']}\n\n\
start time - {data['start_time']}\n\n\
end time - {data['end_time']} \n\n\
answers - {data['answers']} \n\n@current_time_123bot", reply_markup=ReplyKeyboardRemove())



@dp.message_handler(Command("my_tests"))
async def my_tests(message: types.Message, state:FSMContext):
    my_test = await db.select_test_numbers(message.from_user.id)
    my_tests = "test raqami:    test nomi\n"
    print(my_test)
    if my_test:
            
        for test in my_test:
            my_tests +=f"{test[0]}                   |      {test[1]} \n"
            my_tests +="____________________________\n"
    else:
        await message.answer("siz hali test yaratmadingiz \nyaratish uchun /add_test buyrug'ini tanlang")
    
    counts = await db.count_user_tests(message.from_user.id)
    my_tests += f" sizning jami testlariniz soni  {counts}\n\n"
    my_tests += "@current_time_123bot"

    await message.answer(my_tests, reply_markup=ReplyKeyboardRemove())
    await state.set_state("test_results")
    await message.answer("Natijalar bilan ko'rish uchun test raqamini yuboring")
    await message.answer("bekor qilish uchun /start")



@dp.message_handler(state="test_results")
async def my_tests(message: types.Message, state:FSMContext):
    t_number = message.text
    try:

        my_test = await db.select_test_with_results(owner_id=message.from_user.id, test_number=int(t_number))
        print("if dan oldin")
        if my_test:
            print("2 if ga kirdi ")
            full_info = f" Test raqami {my_test[0]}\n Test nomi   {my_test[1]}\n Test javobi  {my_test[2]}\n Boshlanish vaqti  {my_test[3]}\n Tugash vaqti   {my_test[4]}\n"
            dashboard = await db.select_dashboard(int(t_number))
            print(dashboard)
            if dashboard:     
                print("if ga kirish")
                text = f"{int(t_number)} raqamli test natijalari <br>"
                for x in dashboard:
                    text +=f"{x[0]}."
                    text +=f" Ism {x[1]}"
                    text +=f" Javoblar  {x[2]} "
                    text +=f" Natija {x[3]}<br><br>"

            print("shu yerga keldi")
            telegraph = Telegraph()
            print(telegraph.create_account(short_name='Bobir_Mardonov', author_name='Bobir Mardonov', author_url="http://t.me/Bobir_Mardonov"))

            response = telegraph.create_page(f"Qatnashuvchilar reyting test {my_test[0]} {my_test[1]}",html_content=f"<p>{text}</p>")
            urls = response['url']
            
            result_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="natijalarni ko'rish 🚀", url=urls)
                    ],
                ])
            
            await message.answer(full_info,reply_markup=result_button )
            await state.finish
        else:
            await message.answer(f"{int(t_number)} raqamli test sizga tegishli emas yoki unda hech kim qatnashmagan if else da  ")
            await state.finish()

    except:
        await message.answer(f"{int(t_number)} raqamli test sizga tegishli emas yoki unda hech kim qatnashmagan ")
        await state.finish()



@dp.message_handler(Command("update_name"))
async def update_name_state(message:Message, state:FSMContext):
    await message.answer("Testlarda ismingiz telegram ismingiz orqali ro'yxatga olinadi\
 shuning uchun to'liq ismingiz bilan ro'yxatdan o'tishingizni maslahat beramiz \nIsm familyangizni yuboring: \
\nbekor qilish uchun /start buyrug'idan foydalaning!")
    await state.set_state("update_name")

@dp.message_handler(state="update_name")
async def update_name(message: Message, state: FSMContext):
    tetx = message.text
    await db.update_user_full_name(tetx, telegram_id=message.from_user.id)
    await message.answer("Ism Familyangiz muvaffaqiyatli yangilandi!")

