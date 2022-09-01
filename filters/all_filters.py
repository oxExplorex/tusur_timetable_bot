from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import admins

class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return types.ChatType.PRIVATE == message.chat.type

class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in admins:
            return True
        else:
            return False
        