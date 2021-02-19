from aiogram import types
from misc import dp,bot
import asyncio

ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2]

id_chat = 0

@dp.message_handler(content_types='text')
async def all_other_messages(message: types.message):
    if message.chat.id == -1001165927497:
        if ('start=' in message.text) and (message.from_user.id not in ADMIN_ID):
            a = await message.answer(f'Реклама в данном чате запрещена.\n'
                                     f'Кстати, бот которого ты скинул - н@ебалово\n\n'
                                     f'Не будь таким наивным!')
            await asyncio.sleep(7)
            await bot.delete_message(chat_id=message.chat.id, message_id=a.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.message):
    if message.chat.id == -1001165927497:
        await bot.send_message(message.chat.id, f'{message.from_user.first_name}, '
                                                f'добро пожаловать в команду Лучших🤘')