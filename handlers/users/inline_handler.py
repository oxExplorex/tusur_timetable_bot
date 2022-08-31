from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states.state_users import StorageUsers
from keyboards.inline import back_keyboard, start_keyboard

from chrome_tools.selenium_tools import Chrome

from loader import dp, bot


@dp.callback_query_handler(text="delete_message", state="*")
async def delete_message_users(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)

@dp.callback_query_handler(text_startswith="get_https://timetable.tusur.ru/", state="*")
@dp.throttled(rate=3)
async def again_get_timetable(call: CallbackQuery, state: FSMContext):
    find_url = call.data[4:]
    message = call.message
    m = await bot.send_message(message.chat.id, "Начинаю парсинг...")

    http = Chrome()
    result = await http.get_table(find_url)
    if isinstance(result, dict):
        if not result["photo"]:
            await bot.edit_message_text(result['caption'],
                                        m.chat.id, m.message_id,
                                        reply_markup=start_keyboard)
        else:
            await bot.delete_message(m.chat.id, m.message_id)
            await bot.send_photo(message.chat.id,
                                 photo=result['photo'],
                                 caption=result['caption'],
                                 parse_mode="HTML",
                                 reply_markup=result['reply_markup'])
            if result['caption2']:
                await bot.send_message(message.chat.id,
                                       text=result['caption2'],
                                       reply_markup=result['reply_markup2']
                                       )

    else:
        await bot.delete_message(m.chat.id, m.message_id)
        await bot.send_message(message.chat.id,
                               "Ошибка парсинга, попробуйте еще раз",
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

