from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await db.add_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Для регистрации /subscribe\n"
                         f"Отказаться от подписки /unsubscribe")
