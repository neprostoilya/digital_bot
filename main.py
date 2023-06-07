from database import *
from keyboards import *

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, LabeledPrice
import math

import os
from dotenv import *
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
MANAGER = os.getenv('MANAGER')

bot = Bot(TOKEN, parse_mode='HTML') 
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    if message.text == '/start':
        await message.answer(f"Добро пожаловать в диджитал агентство!")           
        await register_user(message)

async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    user = select_user(chat_id)
    if user:
        await message.answer('Авторизация прошла успешно')
        await show_main_menu(message)
    else:
        first_register_user(chat_id, full_name)
        await message.answer("Для регистрации нажмите на кнопку",
                             reply_markup=generate_phone_button())



@dp.message_handler(content_types=['contact']) 
async def finish_register(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    update_user_to_finish_register(phone, chat_id)
    await message.answer("Регистрация прошла успешно")
    await show_main_menu(message)
     

async def show_main_menu(message: Message):
    await message.answer("Какую услугу вы бы хотели заказать? У нас есть следующие варианты:",
                         reply_markup=generate_main_button())
    

@dp.callback_query_handler(lambda call: 'category_' in call.data)
async def show_in_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    category_id = int(call.data.split('_')[1])
    name = select_user(chat_id)[0][1]
    phone = select_user(chat_id)[0][3]
    name_category = get_name_categories(category_id)[0]
    hours = int(get_hours_categories(category_id)[0])
    price = hours * 1400
    days = math.ceil(hours / 6)
    week = math.ceil(days / 5)
    insert_order(name, chat_id, phone, name_category, price, hours, days, week)

    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, text=f"Для выбранной вами услуги стоимость составляет {hours} часов работы." +
                        f" Исходя из этого, примерная стоимость вашего заказа будет: {hours} часов x 1400 рублей/час = {price} рублей." +
                        f" Рабочие дни в неделе: 5. Следовательно, на выполнение задачи мы можем потратить до {week} недель ({days} рабочих дней).")
    
    await bot.send_message(chat_id, text=f"Примерная стоимость вашего заказа составляет {price} рублей, а сроки выполнения - до " +
                           f"{week} недель. Если вы готовы оставить заявку, пожалуйста, подтвердите это.",
                           reply_markup=confirmation_order())

@dp.message_handler(regexp=r'✅ Подтвердить')
async def confermation(message: Message):
    chat_id = message.chat.id
    order = get_order(chat_id)

    text = f'''
Имя заказчика <b>{order[0][1]}</b>
Номер заказчика <b>{order[0][3]}</b>
Название услуги <b>{order[0][4]}</b>
Цена услуги <b>{order[0][5]}</b> рублей
Часов: <b>{order[0][6]}</b>
Дней: <b>{order[0][7]}</b>
Недель: <b>{order[0][8]}</b> 
    '''
    await bot.send_message(MANAGER, text) 
    await message.answer("Отлично! Ваша заявка принята. Мы свяжемся с вами в ближайшее время для уточнения деталей. Спасибо за обращение!")
    await message.answer("Если у вас возникнут еще вопросы или вам понадобится дополнительная информация, не стесняйтесь обращаться. Удачного дня!",
                         reply_markup=main_menu())
    
@dp.message_handler(regexp=r'❎ Отклонить')
async def confermation(message: Message):
    chat_id = message.chat.id
    delete_order(chat_id)
    await show_main_menu(message)

@dp.message_handler(regexp=r'⬅ Назад')

async def back_to_main_menu(message: Message):
    chat_id = message.chat.id
    delete_order(chat_id)
    await show_main_menu(message)
executor.start_polling(dp)
