from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states.state_users import StorageUsers
from keyboards.inline import back_keyboard, start_keyboard

from loader import dp, bot

@dp.callback_query_handler(text="back_button", state="*")
async def back_neutral_state(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.edit_message_text("Расписание группы или преподавателя ТУСУР",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=start_keyboard)

@dp.callback_query_handler(text="user_input", state="*")
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

