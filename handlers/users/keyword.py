import logging

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from filters import AdminFilter
from loader import dp, db
from notify import main
from states.keyword_state import AddKeyword, DeleteKeyword


@dp.message_handler(Command("keywords"), AdminFilter())
async def bot_add(message: types.Message):
    keywords = await db.get_keywords()
    # dic = {}
    text = ""
    for keyword in keywords:
        text += f"{keyword['id']} -> {keyword['title']}\n"
        # dic[keyword['id']] = keyword['title']
    await message.answer(text)


@dp.message_handler(Command("add"), AdminFilter(), state=None)
async def bot_add(message: types.Message):
    await message.answer("Send me a new keyword")
    await AddKeyword.GetKey.set()


@dp.message_handler(AdminFilter(), state=AddKeyword.GetKey)
async def add_keyword(message: types.Message, state: FSMContext):
    new_words = message.text.split(",")
    for word in new_words:
        await db.add_keyword(word.strip())
        await main(new_keyword=word)
    await state.finish()


@dp.message_handler(Command("delete"), AdminFilter(), state=None)
async def bot_add(message: types.Message):
    text = ""
    keywords = await db.get_keywords()
    for keyword in keywords:
        text += f"{keyword['id']} -> {keyword['title']}\n"
    await message.answer(text)
    await message.answer("Choose by id")
    await DeleteKeyword.DeleteKey.set()


@dp.message_handler(AdminFilter(), state=DeleteKeyword.DeleteKey)
async def add_keyword(message: types.Message, state: FSMContext):
    ids = message.text.split(",")
    for id in ids:
        await db.delete_keyword(id=int(id.strip()))
    await message.answer("Deleted successfully!")
    await state.finish()
