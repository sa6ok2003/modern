from aiogram import types
from misc import dp, bot
import sqlite3
from .sqlit import info_members, reg_one_channel, reg_channels
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 1489359560 #Менеджер

ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3]

class reg(StatesGroup):
    name = State()
    fname = State()



@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        await bot.send_message(message.chat.id, 'Hello admin!')
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_b = types.InlineKeyboardButton(text='NEW канал', callback_data='new_channel')# Добавляет 1 канал
        bat_c = types.InlineKeyboardButton(text='NEW Список', callback_data='new_channels') # Добавляет список каналов через пробел
        bat_d = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')  # Рассылка юзерам
        markup.add(bat_a, bat_b, bat_c, bat_d)
        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)



############################   Удаление юзера    ######################################
@dp.message_handler(content_types= 'text')
async def text_admin (message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        del_id = message.forward_from.id
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        sql.execute(f"DELETE FROM user_time WHERE id ={del_id}")
        db.commit()
        await bot.send_message(message.chat.id, 'Удаление выполнено')


############################  REG ONE CHANNEL  ###################################

@dp.callback_query_handler(text='new_channel')  # АДМИН КНОПКА Добавления нового трафика
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название нового канала в формате\n'
                                                 '@name_channel')
    await reg.name.set()


@dp.message_handler(state=reg.name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        reg_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Регистрация успешна')
        await state.finish()


####################################################################################
################################    REG MANY CHANNELS    ###########################

@dp.callback_query_handler(text='new_channels')  # АДМИН КНОПКА Добавления новые телеграмм каналы
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь список каналов в формате\n'
                                                 '@name1 @name2 @name3 ')
    await reg.fname.set()


@dp.message_handler(state=reg.fname, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Каналы зарегистрированы')
    reg_channels(message.text)
    await state.finish()

#####################################################################################


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    a = info_members() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')


########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.st_name.set()



@dp.message_handler(state=st_reg.st_name,content_types=['text','photo','video','video_note'])
async def fname_step(message: types.Message, state: FSMContext):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    a = 0
    for i in sql.execute("SELECT id FROM user_time"):
        a += 1
        if a == 15:
            await asyncio.sleep(10)
        await message.copy_to(i[0])
        await asyncio.sleep(1)

    await state.finish()
    await bot.send_message(message.chat.id, 'Рассылка выполенена!')
#########################################################