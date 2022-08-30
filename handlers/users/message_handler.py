from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from states.state_users import StorageUsers
from keyboards.inline import start_keyboard

from chrome_tools.selenium_tools import Chrome
from bs4 import BeautifulSoup
from loader import dp, bot

import asyncio

@dp.message_handler(state=StorageUsers.input_name)
async def input_name_handler(message: Message, state: FSMContext):
    text = message.text
    condition = len(text) <= 20 and text == "".join([c for c in text if c not in "\\/[]:;'\",.<>?!@#$%^&*()_+=№"])
    if condition:
        async with state.proxy() as data:
            await bot.delete_message(data["input_name"]['chat_id'], data["input_name"]['message_id'])

        find_url = f"https://timetable.tusur.ru/searches/common_search?" \
                   f"utf8=%E2%9C%93" \
                   f"&search%5Bcommon%5D={text}" \
                   f"&commit=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8"

        asyncio.create_task(start_working(message, find_url))

    else:
        async with state.proxy() as data:
            await bot.delete_message(data["input_name"]['chat_id'], data["input_name"]['message_id'])
        await bot.send_message(message.chat.id, "Данный формат не поддерживается :/", reply_markup=start_keyboard)
    await state.finish()

async def start_working(message, find_url):
    try:
        m = await bot.send_message(message.chat.id, "Начинаю парсинг...")
    except:
        return False

    http = Chrome()
    try:
        if await http.get_url(find_url):
            await bot.edit_message_text("Получил страничку", m.chat.id, m.message_id)
            html = await http.get_page_source()
            if "не дал результатов" in html:
                await bot.edit_message_text("Парсинг не дал результатов, повторите попытку",
                                            m.chat.id, m.message_id,
                                            reply_markup=start_keyboard)
            elif "Результаты поиска" in html:
                png = await http.create_choice_png()
                await bot.delete_message(m.chat.id, m.message_id)
                await bot.send_photo(message.chat.id, png, caption="Повторите запрос одним из предложенных вариантов")
            elif "Расписание занятий группы" in html:
                png = await http.create_table_png()
                await bot.delete_message(m.chat.id, m.message_id)

                soup = BeautifulSoup(html, "lxml")
                info = soup.find("title").text
                more_info = soup.find("div", {"class": "col-md-12"}).text.replace("\n", "")

                await bot.send_photo(message.chat.id,
                                     png,
                                     caption=f"{info}\n<code>{more_info}</code>",
                                     parse_mode="HTML")
            elif "Расписание занятий преподавателя" in html:
                png = await http.create_table_png_teacher()
                await bot.delete_message(m.chat.id, m.message_id)

                soup = BeautifulSoup(html, "lxml")
                info = soup.find("title").text
                more_info = soup.find("div", {"class": "col-md-12"}).text.replace("\n", "")

                await bot.send_photo(message.chat.id,
                                     png,
                                     caption=f"{info}\n<code>{more_info}</code>",
                                     parse_mode="HTML")
            else:
                await bot.edit_message_text("Неизвестная ошибка",
                                            m.chat.id, m.message_id,
                                            reply_markup=start_keyboard)
        else:
            await bot.delete_message(m.chat.id, m.message_id)
            await bot.send_message("Ошибка парсинга, попробуйте еще раз", reply_markup=start_keyboard)
    except Exception as e:
        print(e)
    await http.driver_quit()

