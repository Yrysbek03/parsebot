import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

with open("new_episode.json", 'r') as f:
    new = json.load(f)

if len(new) > 0:
    watch = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="смотреть", url=new[0]['link'], callback_data="watch")
            ]
        ]
    )
else:
    watch = InlineKeyboardMarkup(
        inline_keyboard=[
            [

            ]
        ]
    )