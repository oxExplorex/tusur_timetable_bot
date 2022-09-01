from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards.inline import start_keyboard
from loader import dp, bot

from utils.db_api.sqlite import *


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    get_user_id = get_user(user_id=message.from_user.id)
    if not get_user_id:
        create_users(message.from_user.id)

    await bot.send_message(message.chat.id,
                           "Расписание группы или преподавателя ТУСУР",
                           reply_markup=start_keyboard)
