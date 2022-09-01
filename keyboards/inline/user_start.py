from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup()
start_keyboard.add(InlineKeyboardButton(text="Ввести группу или ФИО преподавателя", callback_data="user_input"))
start_keyboard.add(InlineKeyboardButton(text="Настроить быстрый ввод (only admin)", callback_data="setting_group"))
start_keyboard.add(InlineKeyboardButton(text="Подписаться на расписание (only admin)", callback_data="subject_timetable"))


back_keyboard = InlineKeyboardMarkup()
back_keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="back_button"))

