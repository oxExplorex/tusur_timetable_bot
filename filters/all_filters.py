from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import admins

# Проверка на написания сообщения в ЛС бота
class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return types.ChatType.PRIVATE == message.chat.type

# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in admins:
            return True
        else:
            return False