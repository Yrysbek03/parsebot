import json

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db


@dp.message_handler(commands=["subscribe"])
async def bot_start(message: types.Message):
    await db.add_user(id=message.from_user.id, login=message.from_user.username, subscription=True)
    await db.sql_update_subscription(message.from_user.id)
    await message.answer(f"Ура, вы зарегистрировались!")


@dp.message_handler(commands=["unsubscribe"])
async def bot_start(message: types.Message):
    await db.sql_update_subscription(message.from_user.id, False)
    await message.answer(f"Вы отменили подписку!")
