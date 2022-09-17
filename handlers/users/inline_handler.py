from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states.state_users import StorageUsers
from keyboards.inline import back_keyboard, start_keyboard, wait_keyboard

from chrome_tools.selenium_tools import Chrome

from utils.db_api.sqlite import select_fast_answer_by_url, create_fast_answer_by_request, \
    update_fast_answer_information

from urllib.parse import unquote
from utils.times import get_time_now
from loader import dp, bot

import ujson

@dp.callback_query_handler(text="delete_message", state="*")
async def delete_message_users(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)

@dp.callback_query_handler(text_startswith="upd_", state="*")
@dp.throttled(rate=10)
async def update_timetable_by_button(call: CallbackQuery):
    find_url = "https://timetable.tusur.ru" + unquote(call.data[4:])
    find_url = find_url.replace(':sc:', '/searches/common_search')

    m = call.message

    await bot.edit_message_caption(
                                   m.chat.id, m.message_id,
                                   caption="Обновление...",
                                   reply_markup=wait_keyboard)

    http = Chrome()
    result = await http.get_table(find_url)

    if isinstance(result, dict):
        if not result["photo"]:
            await bot.edit_message_caption(result['caption'],
                                           m.chat.id, m.message_id,
                                           reply_markup=start_keyboard)
        else:
            await bot.delete_message(m.chat.id, m.message_id)
            message_photo = await bot.send_photo(m.chat.id,
                                 photo=result['photo'],
                                 caption=result['caption'] + \
                                         f"\n\n<code>Последнее обновление: {result['last_update']}</code>",
                                 parse_mode="HTML",
                                 reply_markup=result['reply_markup'])
            result['photo'] = message_photo['photo'][0]['file_id']

            if result['caption2']:
                await bot.send_message(m.chat.id,
                                       text=result['caption2'],
                                       reply_markup=result['reply_markup2']
                                       )

        get_info_by_url = select_fast_answer_by_url(find_url)
        if not get_info_by_url:
            create_fast_answer_by_request("", str(result), result["end_link"])
        else:
            update_fast_answer_information(result["end_link"], get_info_by_url[0][0], str(result))
    else:
        last_message = select_fast_answer_by_url(find_url)
        result = ujson.loads(last_message[0][1].replace("'", '"'))
        await bot.delete_message(m.chat.id, m.message_id)
        await bot.send_message(m.chat.id,
                               text="Ошибка парсинга, попробуйте еще раз",
                               reply_markup=result['reply_markup'])



@dp.callback_query_handler(text_startswith="get_", state="*")
@dp.throttled(rate=2)
async def again_get_timetable(call: CallbackQuery, state: FSMContext):
    find_url = "https://timetable.tusur.ru" + unquote(call.data[4:])
    message = call.message

    get_info_by_url = select_fast_answer_by_url(find_url)

    new_find = False

    m = await bot.send_message(message.chat.id, "Начинаю парсинг...")

    if not get_info_by_url or \
            (get_time_now() != get_info_by_url[0][3]) or \
            ("error" in ujson.loads(get_info_by_url[0][1].replace("'", '"'))):

        new_find = True

        http = Chrome()
        result = await http.get_table(find_url)
    else:
        result = ujson.loads(get_info_by_url[0][1].replace("'", '"'))

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
            if not get_info_by_url:
                create_fast_answer_by_request("", str(result), result["end_link"])
            else:
                update_fast_answer_information(result["end_link"], get_info_by_url[0][0], str(result))
    else:
        await bot.delete_message(m.chat.id, m.message_id)
        await bot.send_message(message.chat.id,
                               text="Ошибка парсинга, попробуйте еще раз",
                               reply_markup=start_keyboard)



@dp.callback_query_handler(text="back_button", state="*")
async def back_neutral_state(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.edit_message_text("Расписание группы или преподавателя ТУСУР",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=start_keyboard)

@dp.callback_query_handler(text="user_input", state="*")
@dp.throttled(rate=3)
async def input_group_name(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text("Введите группу или ФИО преподавателя",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=back_keyboard)
    await StorageUsers.input_name.set()
    async with state.proxy() as data:
        data["input_name"] = {"chat_id": call.message.chat.id,
                              "message_id": call.message.message_id
        }

