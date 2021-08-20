import asyncio
import logging

import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup

from loader import db, dp

limit = 15


async def check(mainBlog, new_keyword):
    if new_keyword is None:
        keywords = await db.get_keywords()
    for blog in mainBlog:
        if new_keyword is None:
            for keyword in keywords:
                if keyword['title'].lower().replace(" ", '') in blog.get_text(strip=True).lower().replace(" ", ''):
                    return True
        else:
            if new_keyword.lower().replace(" ", '') in blog.get_text(strip=True).lower().replace(" ", ''):
                return True
    return False


async def parseLada(url, className, new_keyword):
    keywords = await db.get_keywords()
    html = BeautifulSoup(requests.get(url).content, 'lxml').find(class_=className)
    if html is None:
        return False
    blog = html.get_text(strip=True).lower().replace(' ', '')
    for keyword in keywords:
        if keyword['title'].lower().replace(" ", '') in blog.lower().replace(" ", ''):
            return True
        # if keyword.lower().replace(" ", '') in blog:
        #     return True
    return False


async def parse(url, className, new_keyword):
    html = BeautifulSoup(requests.get(url).content, 'lxml').find(class_=className)
    if html is None:
        return False
    blogs_p = html.find_all('p')
    blogs_q = html.find_all('blockquote')
    return await check(blogs_p, new_keyword) or await check(blogs_q, new_keyword)


async def azattyq(new_keyword=None):
    last_link = ""
    if new_keyword is None:
        last_link = (await db.get_website(name="azattyq"))['last_link']
        new_last_link = last_link
    html = BeautifulSoup(requests.get('https://www.azattyq.org/z/330').content, 'lxml')
    cnt = 0
    for to in html.find_all(class_='col-xs-12 col-sm-12 col-md-12 col-lg-12 fui-grid__inner'):
        # print("azattyq", 'https://www.azattyq.org' + to.div.a['href'])
        cnt += 1
        if cnt > limit or 'https://www.azattyq.org' + to.div.a['href'] == last_link and new_keyword is None:
            break
        if cnt == 1:
            new_last_link = 'https://www.azattyq.org' + to.div.a['href']
        if await parse('https://www.azattyq.org' + to.div.a['href'], 'content-floated-wrap fb-quotable', new_keyword):
            users = await db.sql_get_all_users()
            for user in users:
                await dp.bot.send_message(user[0], f"{to.div.a.h4}",
                                          reply_markup=InlineKeyboardMarkup(
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(text="view",
                                                                           url='https://www.azattyq.org' + to.div.a[
                                                                               'href'],
                                                                           callback_data='view')
                                                  ]
                                              ]
                                          ))
    if new_keyword is None:
        await db.update_website(name="azattyq", last_link=new_last_link)


async def azattyqruhy(new_keyword=None):
    last_link = ""
    try:
        if new_keyword is None:
            last_link = (await db.get_website(name="azattyqruhy"))['last_link']
            new_last_link = last_link
        html = BeautifulSoup(requests.get('https://www.azattyq-ruhy.kz/news').content, 'lxml')
        cnt = 0
        for to in html.findAll('a'):
            # print("azattyqruhy", to['href'])
            if '/news/' not in to['href']:
                continue
            cnt += 1
            if cnt > limit or to['href'] == last_link and new_keyword is None:
                break
            if cnt == 1:
                new_last_link = to['href']
            if await parse(to['href'], 'news_view__text lg-mb-20 xs-pl-15 xs-pr-15', new_keyword):
                users = await db.sql_get_all_users()
                for user in users:
                    await dp.bot.send_message(user[0], f"{to.img['title'].text.strip()}",
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(text="view",
                                                                               url=to['href'],
                                                                               callback_data='view')
                                                      ]
                                                  ]
                                              ))
        if new_keyword is None:
            await db.update_website(name="azattyqruhy", last_link=new_last_link)
    except Exception as e:
        logging.info(e)


async def inaktau(new_keyword=None):
    last_link = ""
    try:
        if new_keyword is None:
            last_link = (await db.get_website(name="inaktau"))['last_link']
            new_last_link = last_link
        html = BeautifulSoup(requests.get('https://www.inaktau.kz/').content, 'lxml')
        blocks = html.find_all(class_='card-wrapper col-12 col-sm-6 col-md-4 col-lg-3')
        cnt = 0
        for block in blocks:
            # print("inaktau", block.div.a['href'])
            if 'news' not in str(block.div.a):
                continue
            if block.div.a['href'] == last_link:
                break
            if cnt > limit or new_last_link == last_link and new_keyword is None:
                new_last_link = block.div.a['href']
            if await parse(block.div.a['href'], 'article-text', new_keyword):
                users = await db.sql_get_all_users()
                for user in users:
                    await dp.bot.send_message(user[0], f"{block.div.a.text.strip()}",
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(text="view",
                                                                               url=block.div.a['href'],
                                                                               callback_data='view')
                                                      ]
                                                  ]
                                              ))
        if new_keyword is None:
            await db.update_website(name="inaktau", last_link=new_last_link)
    except Exception as e:
        logging.info(e)


async def tengrinews(new_keyword=None):
    last_link = ""
    if new_keyword is None:
        last_link = (await db.get_website(name="tengrinews"))['last_link']
        new_last_link = last_link
    html = BeautifulSoup(requests.get('https://tengrinews.kz/').content, 'lxml')
    blocks = html.find_all(class_='tn-tape-item')
    cnt = 0
    for block in blocks:
        # print("tengrinews", 'https://tengrinews.kz' + block.a['href'])
        if 'http' in block.a['href']:
            continue
        cnt += 1
        if cnt > limit or 'https://tengrinews.kz' + block.a['href'] == last_link and new_keyword is None:
            break
        if cnt == 1:
            new_last_link = 'https://tengrinews.kz' + block.a['href']
        if await parse('https://tengrinews.kz' + block.a['href'], 'tn-news-text', new_keyword):
            users = await db.sql_get_all_users()
            for user in users:
                await dp.bot.send_message(user[0], f"{block.find(class_='tn-tape-item').get_text(strip=True)}",
                                          reply_markup=InlineKeyboardMarkup(
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(text="view",
                                                                           url='https://tengrinews.kz' + block.a[
                                                                               'href'],
                                                                           callback_data='view')
                                                  ]
                                              ]
                                          ))
    if new_keyword is None:
        await db.update_website(name="tengrinews", last_link=new_last_link)


async def lada(new_keyword=None):
    last_link = ""
    if new_keyword is None:
        last_link = (await db.get_website(name="lada"))['last_link']
        new_last_link = last_link
    html = BeautifulSoup(requests.get('https://www.lada.kz/lastnews/').content, 'lxml')
    blocks = html.find_all(class_='cat-shortstory')
    cnt = 0
    for block in blocks:
        # print('lada', block.div.a['href'])
        cnt += 1
        if cnt > limit or block.div.a['href'] == last_link and new_keyword is None:
            break
        if cnt == 1:
            new_last_link = block.div.a['href']
        if await parseLada(block.div.a['href'], 'article-fulltext', new_keyword):
            users = await db.sql_get_all_users()
            for user in users:
                await dp.bot.send_message(user[0], f"{block.h2.text.strip()}",
                                          reply_markup=InlineKeyboardMarkup(
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(text="view",
                                                                           url=block.div.a['href'],
                                                                           callback_data='view')
                                                  ]
                                              ]
                                          ))
    if new_keyword is None:
        await db.update_website(name="lada", last_link=new_last_link)


async def inform(new_keyword=None):
    last_link = ""
    html = BeautifulSoup(requests.get('https://lenta.inform.kz/ru').content, 'lxml')
    if new_keyword is None:
        last_link = (await db.get_website(name="inform"))['last_link']
        new_last_link = last_link
    blocks = html.find_all(class_='lenta_news_block')
    cnt = 0
    for block in blocks:
        cnt += 1
        if 'https://lenta.inform.kz' + block.a['href'] == last_link and new_keyword is None or cnt > limit:
            break
        if cnt == 1:
            new_last_link = 'https://lenta.inform.kz' + block.a['href']
        if await parse('https://lenta.inform.kz' + block.a['href'], 'article_body', new_keyword):
            users = await db.sql_get_all_users()
            for user in users:
                await dp.bot.send_message(user[0], f"{block.find(class_='lenta_news_title').get_text(strip=True)}",
                                          reply_markup=InlineKeyboardMarkup(
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(text="view",
                                                                           url='https://lenta.inform.kz' + block.a[
                                                                               'href'],
                                                                           callback_data='view')
                                                  ]
                                              ]
                                          ))
    if new_keyword is None:
        await db.update_website(name="inform", last_link=new_last_link)


async def informburo(new_keyword=None):
    last_link = ""
    html = BeautifulSoup(requests.get('https://informburo.kz/novosti').content, 'lxml')
    if new_keyword is None:
        last_link = (await db.get_website(name="informburo"))['last_link']
        new_last_link = last_link
    blocks = html.find('ul', class_='uk-nav uk-nav-default')
    cnt = 0
    for block in blocks.select('li'):
        # print(block.a['href'])
        cnt += 1
        if cnt > limit or block.a['href'] == last_link and new_keyword is None:
            break
        if cnt == 1:
            new_last_link = block.a['href']
        if await parse(block.a['href'], 'article', new_keyword):
            users = await db.sql_get_all_users()
            for user in users:
                await dp.bot.send_message(user[0], f'{block.a.text.strip()}',
                                          reply_markup=InlineKeyboardMarkup(
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(text="view", url=block.a['href'],
                                                                           callback_data='view')
                                                  ]
                                              ]
                                          ))
    if new_keyword is None:
        await db.update_website(name="informburo", last_link=new_last_link)


async def kzinform(new_keyword=None):
    last_link = ""
    html = BeautifulSoup(requests.get('https://kzinform.com/').content, 'lxml')
    if new_keyword is None:
        last_link = (await db.get_website(name="kzinform"))['last_link']
        new_last_link = last_link
    blocks = html.find(class_='dd bg')
    cnt = 0
    for block in blocks.select('a'):
        cnt += 1
        if cnt > limit or block['href'] == last_link and new_keyword is None:
            break
        if cnt == 1:
            new_last_link = block['href']
        if await parse(block['href'], 'article', new_keyword):
            users = await db.sql_get_all_users()
            for user in users:
                await dp.bot.send_message(user[0], f'{block.span.text.strip()}',
                                          reply_markup=InlineKeyboardMarkup(
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(text="view", url=block['href'],
                                                                           callback_data='view')
                                                  ]
                                              ]
                                          ))
    if new_keyword is None:
        await db.update_website(name="kzinform", last_link=new_last_link)


async def nur(new_keyword=None):
    last_link = ""
    html = BeautifulSoup(requests.get('https://www.nur.kz/latest/').content, 'lxml')
    if new_keyword is None:
        last_link = (await db.get_website(name="nur"))['last_link']
        new_last_link = last_link
    blocks = (html.find(class_='block-infinite js-infinite')).select('ul')
    cnt = 0
    for to in blocks:
        for block in to.select('li'):
            cnt += 1
            if cnt > limit or block.article.a['href'] == last_link and new_keyword is None:
                break
            if cnt == 1:
                new_last_link = block.article.a['href']
            if await parse(block.article.a['href'], 'formatted-body io-article-body js-article-body', new_keyword):

                # print(block.article.a['href'])
                users = await db.sql_get_all_users()
                for user in users:
                    await dp.bot.send_message(user[0], f'{block.article.a.h2.text.strip()}',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(text="view", url=block.article.a['href'],
                                                                               callback_data='view')
                                                      ]
                                                  ]
                                              ))
    if new_keyword is None:
        await db.update_website(name="nur", last_link=new_last_link)


async def time(new_keyword=None):
    last_link = ""
    html = BeautifulSoup(requests.get('https://time.kz/blogs').content, 'lxml')
    if new_keyword is None:
        last_link = (await db.get_website(name="time"))['last_link']
        new_last_link = last_link
    blocks = html.find_all(class_='col-12 col-md-6 order-3 order-md-2')
    cnt = 0
    for block in blocks:
        cnt += 1
        if cnt > limit or 'https://time.kz' + block.h3.a['href'] == last_link and new_keyword is None:
            break
        if cnt == 1:
            new_last_link = 'https://time.kz' + block.h3.a['href']
        if await parse('https://time.kz/' + block.h3.a['href'], 'col-md-12 col-lg-8 post__text user-content',
                       new_keyword):
            users = await db.sql_get_all_users()
            for user in users:
                await dp.bot.send_message(user[0], f'{block.h3.a.text.strip()}',
                                          reply_markup=InlineKeyboardMarkup(
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(text="view",
                                                                           url='https://time.kz/' + block.h3.a['href'],
                                                                           callback_data='view')
                                                  ]
                                              ]
                                          ))
    if new_keyword is None:
        await db.update_website(name="time", last_link=new_last_link)


async def total(new_keyword=None):
    cnt = 0
    if new_keyword is None:
        last_link = (await db.get_website(name="total"))['last_link']
        new_last_link = last_link
    for page in range(1, 5):
        last_link = ""

        html = BeautifulSoup(requests.get('https://total.kz/ru/news/page-' + str(page)).content, 'lxml')
        blocks = html.find_all(class_='b-news-list__item')
        can_leave = False
        for block in blocks:
            cnt += 1
            if cnt > limit or 'https://total.kz' + block.a['href'] == last_link and new_keyword is None:
                can_leave = True
                break
            if cnt == 1:
                new_last_link = 'https://total.kz' + block.a['href']
            if await parse('https://total.kz' + block.a['href'], 'article__post__body', new_keyword):
                users = await db.sql_get_all_users()
                for user in users:
                    await dp.bot.send_message(user[0], f'{block.h3.text.strip()}',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(text="view",
                                                                               url='https://total.kz' + block.a['href'],
                                                                               callback_data='view')
                                                      ]
                                                  ]
                                              ))
        if can_leave:
            break
    if new_keyword is None:
        await db.update_website(name="total", last_link=new_last_link)


async def zakon(new_keyword=None):
    last_link = ""
    html = BeautifulSoup(requests.get('https://www.zakon.kz/news/').content, 'lxml')
    if new_keyword is None:
        last_link = (await db.get_website(name="zakon"))['last_link']
        new_last_link = last_link
    blocks = html.find_all(class_='cat_news_item')
    cnt = 0
    for block in blocks:
        if '</a>' in str(block):
            cnt += 1
            if cnt > limit or 'https://zakon.kz' + block.a['href'] == last_link and new_keyword is None:
                break
            if cnt == 1:
                new_last_link = 'https://zakon.kz' + block.a['href']
            if await parse('https://zakon.kz' + block.a['href'], 'newscont', new_keyword):
                users = await db.sql_get_all_users()
                for user in users:
                    await dp.bot.send_message(user[0], f'{block.a.text.strip()}',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(text="view",
                                                                               url='https://zakon.kz' + block.a['href'],
                                                                               callback_data='view')
                                                      ]
                                                  ]
                                              ))
    if new_keyword is None:
        await db.update_website(name="zakon", last_link=new_last_link)


def clear():
    with open('inform.txt', 'w', encoding='utf-8') as file:
        file.write('nothing')
    with open('informburo.txt', 'w', encoding='utf-8') as file:
        file.write('nothing')
    with open('kzinform.txt', 'w', encoding='utf-8') as file:
        file.write('nothing')
    with open('nur.txt', 'w', encoding='utf-8') as file:
        file.write('nothing')
    with open('time.txt', 'w', encoding='utf-8') as file:
        file.write('nothing')
    with open('total.txt', 'w', encoding='utf-8') as file:
        file.write('nothing')
    with open('total.txt', 'w', encoding='utf-8') as file:
        file.write('nothing')


if __name__ == '__main__':
    clear()
    print('clean now')
    inform()
    print('inform done')
    informburo()
    print('informburo done')
    kzinform()
    print('kzinform done')
    nur()
    print('nur done')
    time()
    print('time done')
    total()
    print('total done')
    zakon()
    print('zakon done')
