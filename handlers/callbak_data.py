from aiogram import types
from misc import dp, bot
from .sqlit import proverka_channel
name_channel_1 = 'higififfu'
name_channel_2 = 'movie_bots'
name_channel_3 = 'name3'


@dp.callback_query_handler(text_startswith='start_watch')  # Нажал кнопку Начать смотреть
async def start_watch(call: types.callback_query):
    name_channel = call.data[12:]

    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤', callback_data=f'check{name_channel}')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, '❌ ДОСТУП ЗАКРЫТ ❌\n\n '
                                                     '👉Для доступа к приватному каналу нужно быть подписчиком <b>Кино-каналов.</b>\n\n'
                                                     'Подпишись на <b>каналы</b> ниже 👇 и нажми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!\n\n'
                                                     f'<b>Канал 1</b> - https://t.me/{name_channel_1}\n'
                                                     f'<b>Канал 2</b> - https://t.me/{name_channel_2}\n'
                                                     f'<b>Канал 3</b> - https://t.me/{name_channel_3}', parse_mode='html',reply_markup=markup)




@dp.callback_query_handler(text_startswith='check')  # Нажал кнопку Я ПОДПИСАЛСЯ. ДЕЛАЕМ ПРОВЕРКУ
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, '⏳ Ожидайте. Идёт проверка подписки.')
    name_channel = call.data[5:]

    proverka1 = 'member'
    proverka2 = 'member'
    proverka3 = 'member'

    #proverka1 = (await bot.get_chat_member(chat_id=f'@{name_channel_1}', user_id=call.message.chat.id)).status
    #proverka2 = (await bot.get_chat_member(chat_id=f'@{name_channel_2}', user_id=call.message.chat.id)).status
    #proverka3 = (await bot.get_chat_member(chat_id=f'@{name_channel_3}', user_id=call.message.chat.id)).status

    print(proverka1,proverka2,proverka3)

    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥤Я ПОДПИСАЛСЯ🥤', callback_data=f'check{name_channel}')
    markup.add(bat_a)

    if proverka1 == 'member' and proverka2 == 'member' and proverka3 == 'member': #Человек прошел все 3 проверки
        if name_channel == '':
            ######  Человек перещел без реферальной ссылке    #####
            markup_2 = types.InlineKeyboardMarkup()
            bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤',
                                               url=f'https://t.me/sanyar_boy')  # Cсылка на приват канал # ВАЖНО!!!!!
            markup_2.add(bat_b)
            await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                         'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',parse_mode='html', reply_markup=markup_2)


            ###########   Человек перешел по реферальной ссылке    ##########

        else:
            #### Здесь нужно реализовать проверку реферальной ссылке - Входит ли она в список или нет   ####
            status = proverka_channel(name_channel) ## Возвращает 1, если телеграмм канал проверен. 0 - Если нет

            if status == 0:
                markup_2 = types.InlineKeyboardMarkup()
                bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤',
                                                   url=f'https://t.me/sanyar_boy')  # ВАЖНО!!!!!
                markup_2.add(bat_b)
                await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                             'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',
                                       parse_mode='html', reply_markup=markup_2)
            else:
                markup_2 = types.InlineKeyboardMarkup()
                bat_b = types.InlineKeyboardButton(text='🥤ПОДПИСАТЬСЯ🥤', url=f'https://t.me/{name_channel}') # Cсылка на приват канал
                markup_2.add(bat_b)
                await bot.send_message(call.message.chat.id, '✅ ДОСТУП ОТКРЫТ\n\n'
                                                             'Все новинки 2021 сливаем на наш приватный канал.<b> Подпишись</b> 👇',parse_mode='html',reply_markup=markup_2)



    else:
        await bot.send_message(call.message.chat.id, '❌Вы не подписались на каналы ниже\n\n'
                                                     'Проверьте еще раз подписку на всех каналах. И нажми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!\n\n'
                                                     f'<b>Канал 1</b> - https://t.me/{name_channel_1}\n'
                                                     f'<b>Канал 2</b> - https://t.me/{name_channel_2}\n'
                                                     f'<b>Канал 3</b> - https://t.me/{name_channel_3}\n', parse_mode='html',reply_markup=markup)



