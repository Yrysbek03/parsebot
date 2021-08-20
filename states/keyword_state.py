from aiogram.dispatcher.filters.state import StatesGroup, State


class AddKeyword(StatesGroup):
    GetKey = State()


class DeleteKeyword(StatesGroup):
    DeleteKey = State()
