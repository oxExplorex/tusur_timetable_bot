from utils.set_bot_commands import set_default_commands

from handlers import dp
import middlewares
import filters

from aiogram import executor
from loguru import logger


async def on_startup(dp):
    filters.setup(dp)
    middlewares.setup(dp)

    await set_default_commands(dp)
    logger.info("Bot was started")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)

