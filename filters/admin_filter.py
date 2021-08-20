from abc import ABC

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        admins = ADMINS
        if message.from_user.id in admins:
            return True
        else:
            return False
