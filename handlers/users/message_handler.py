import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile

from states.state_users import StorageUsers
from keyboards.inline import start_keyboard

from chrome_tools.selenium_tools import Chrome

from utils.db_api.sqlite import select_fast_answer_by_request, create_fast_answer_by_request, \
    select_fast_answer_by_url, update_fast_answer_information, update_fast_answer_information_by_text

from utils.times import get_time_now

from loader import dp, bot
import ujson


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

        get_info_by_text = select_fast_answer_by_request(text)

        new_find = False

        m = await bot.send_message(message.chat.id, "Начинаю парсинг...")

        if not get_info_by_text or \
                (get_time_now() != get_info_by_text[0][3]) or \
                ("error" in ujson.loads(get_info_by_text[0][1].replace("'", '"'))):

            new_find = True

            http = Chrome()
            result = await http.get_table(find_url)
        else:
            result = ujson.loads(get_info_by_text[0][1].replace("'", '"'))

        if isinstance(result, dict):
            if not result["photo"]:
                await bot.edit_message_text(result['caption'],
                                            m.chat.id, m.message_id,
                                            reply_markup=start_keyboard)
            else:
                await bot.delete_message(m.chat.id, m.message_id)
                message_photo = await bot.send_photo(message.chat.id,
                                     photo=result['photo'],
                                     caption=result['caption'] + \
                                             f"\n\n<code>Последнее обновление: {result['last_update']}</code>",
                                     parse_mode="HTML",
                                     reply_markup=result['reply_markup'])
                result['photo'] = message_photo['photo'][0]['file_id']

                if result['caption2']:
                    await bot.send_message(message.chat.id,
                                           text=result['caption2'],
                                           reply_markup=result['reply_markup2']
                                           )

            if new_find:
                end_link = result["end_link"]
                result = str(result)
                if select_fast_answer_by_url(end_link):
                    update_fast_answer_information(end_link, text, result)
                elif get_info_by_text:
                    update_fast_answer_information_by_text(text, end_link, result)
                else:
                    create_fast_answer_by_request(text, result, end_link)
        else:
            await bot.delete_message(m.chat.id, m.message_id)
            await bot.send_message(message.chat.id,
                                   text="Ошибка парсинга, попробуйте еще раз",
                                   reply_markup=start_keyboard)

    else:
        async with state.proxy() as data:
            await bot.delete_message(data["input_name"]['chat_id'],
                                     data["input_name"]['message_id'])
        await bot.send_message(message.chat.id,
                               "Данный формат не поддерживается :/",
                               reply_markup=start_keyboard)
    await state.finish()


