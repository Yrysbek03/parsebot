import asyncio
import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup as bs
from loader import dp, db


async def time_kz_parse(url, new_keyword=None):
    html = bs(requests.get(url).content, 'lxml')
    blogs = html.find_all('p')
    if new_keyword is None:
        keywords = await db.get_keywords()
        # with open('keywords.txt', 'r', encoding='utf-8') as file:
        #     keywords = file.read()
    for blog in blogs:
        if new_keyword is None:
            for keyword in keywords:
                if keyword.lower().replace(" ", '') in blog.get_text(strip=True).lower().replace(" ", ''):
                    return keyword
        else:
            if new_keyword.lower().replace(" ", '') in blog.get_text(strip=True).lower().replace(" ", ''):
                return new_keyword
    return 'no'


async def time_kz(new_keyword=None):
    await asyncio.sleep(15)
    users = await db.sql_get_all_users()
    html = bs(requests.get('https://time.kz/blogs').content, 'lxml')
    if new_keyword is None:
        last_title = await db.get_website(name="time")
        # with open('time_kz.txt', 'r', encoding='utf-8') as file:
        #     last_title = file.read().strip()
    blocks = html.find_all(class_='col-12 col-md-6 order-3 order-md-2')
    for block in blocks:
        if new_keyword is None and block.h3.a.text.strip() == last_title:
            break
        link = 'https://time.kz/' + f"{block.h3.a['href']}"
        request = time_kz_parse(link, new_keyword)
        if request != 'no':
            for user in users:
                await dp.bot.send_message(user[0], f'{block.h3.a.text.strip()}',
                                          reply_markup=InlineKeyboardMarkup(
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(text="view", url=link,
                                                                           callback_data='view')
                                                  ]
                                              ]
                                          ))
    # with open('time_kz.txt', 'w', encoding='utf-8') as file:
    #     file.write(html.find(class_='col-12 col-md-6 order-3 order-md-2').h3.a.text)
    await db.update_website(name="tile", last_title=html.find(class_='col-12 col-md-6 order-3 order-md-2').h3.a.text)
