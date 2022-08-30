from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup()
start_keyboard.add(InlineKeyboardButton(text="Ввести группу или ФИО преподавателя", callback_data="user_input"))

back_keyboard = InlineKeyboardMarkup()
back_keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="back_button"))

