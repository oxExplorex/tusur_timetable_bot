from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup()
start_keyboard.add(InlineKeyboardButton(text="Ввести группу или ФИО преподавателя", callback_data="user_input"))
start_keyboard.add(InlineKeyboardButton(text="Настроить быстрый ввод (only admin)", callback_data="setting_group"))
# start_keyboard.add(InlineKeyboardButton(text="Подписаться на расписание (only admin)", callback_data="subject_timetable"))


wait_keyboard = InlineKeyboardMarkup()
wait_keyboard.add(InlineKeyboardButton(text="Ожидайте", callback_data="12345"))

# update
def update_button_by_url(url):
    url = url.replace('https://timetable.tusur.ru', '')
    url = url.replace('/searches/common_search', ':sc:')
    return InlineKeyboardButton(text="Обновить", callback_data=f"upd_{url}")


# back_button
back_keyboard = InlineKeyboardMarkup()
back_keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="back_button"))

# delete_button
delete_button = InlineKeyboardButton(text="✖️", callback_data="delete_message")
