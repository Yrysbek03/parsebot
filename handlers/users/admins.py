import time

from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import AdminFilter
from loader import dp, db


@dp.message_handler(Command("get", prefixes="!/"), AdminFilter())
async def is_admin(message: types.Message):
    users = await db.sql_get_all_users()
    subscribers = 0
    for user in users:
        if user[2] == 1:
            subscribers += 1
    await message.answer(f"Number of users: {len(users)}\n"
                         f"Number of subscribers: {subscribers}\n"
                         f"{time.asctime()}")
