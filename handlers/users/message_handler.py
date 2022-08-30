from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from states.state_users import StorageUsers
from keyboards.inline import start_keyboard

from chrome_tools.selenium_tools import Chrome
from bs4 import BeautifulSoup
from loader import dp, bot
from loguru import logger
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


        m = await bot.send_message(message.chat.id, "Начинаю парсинг...")

        http = Chrome()
        result = await http.get_table(find_url)
        if isinstance(result, dict):
            if not result["photo"]:
                await bot.edit_message_text(result['caption'],
                                            m.chat.id, m.message_id,
                                            reply_markup=start_keyboard)
            else:
                await bot.send_photo(message.chat.id,
                                     result['photo'],
                                     caption=result['caption'],
                                     parse_mode="HTML")
        else:
            await bot.delete_message(m.chat.id, m.message_id)
            await bot.send_message(message.chat.id,
                                   "Ошибка парсинга, попробуйте еще раз",
                                   reply_markup=start_keyboard)

    else:
        async with state.proxy() as data:
            await bot.delete_message(data["input_name"]['chat_id'], data["input_name"]['message_id'])
        await bot.send_message(message.chat.id, "Данный формат не поддерживается :/", reply_markup=start_keyboard)
    await state.finish()


