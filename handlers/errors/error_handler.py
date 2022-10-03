import logging

from aiogram.types import Update
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError, UserDeactivated,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter, CantParseEntities, MessageCantBeDeleted,
                                      TerminatedByOtherGetUpdates, BotBlocked)
from loguru import logger
from loader import dp

import traceback

@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        logger.error(exception)
        return True

    # Не удалось изменить сообщение
    if isinstance(exception, MessageNotModified):
        logger.error(exception)
        return True

    # Блокировка бота пользователем
    if isinstance(exception, BotBlocked):
        return True

    # Не удалось удалить сообщение
    if isinstance(exception, MessageCantBeDeleted):
        logger.error(exception)
        return True

    # Сообщение для удаления не было найдено
    if isinstance(exception, MessageToDeleteNotFound):
        logger.error(exception)
        return True

    # Сообщение пустое
    if isinstance(exception, MessageTextIsEmpty):
        logger.error(exception)
        return True

    # Пользователь удалён
    if isinstance(exception, UserDeactivated):
        logger.error(exception)
        return True

    # Бот не авторизован
    if isinstance(exception, Unauthorized):
        logger.error(exception)
        return True

    # Неверный Query ID
    if isinstance(exception, InvalidQueryID):
        logger.error(exception)
        return True

    # Повторите попытку позже
    if isinstance(exception, RetryAfter):
        logger.error(exception)
        return True

    # Уже имеется запущенный бот
    if isinstance(exception, TerminatedByOtherGetUpdates):
        print("You already have an active bot. Turn it off.")
        logger.error(exception)
        return True

    # Ошибка в HTML/MARKDOWN разметке
    if isinstance(exception, CantParseEntities):
        logger.error(exception)
        await Update.get_current().message.answer(f"❗ Ошибка HTML разметки\n"
                                                  f"`▶ {exception.args}`\n"
                                                  f"❕ Выполните заново действие с правильной разметкой тэгов.",
                                                  parse_mode="Markdown")
        return True


    logger.error(exception)
    print(traceback.format_exc())
