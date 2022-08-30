# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup

class StorageUsers(StatesGroup):
    input_name = State()

