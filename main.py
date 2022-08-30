from aiogram import executor

import filters
import middlewares
from handlers import dp

from utils.set_bot_commands import set_default_commands

async def on_startup(dp):
    filters.setup(dp)
    middlewares.setup(dp)

    await set_default_commands(dp)
    print("~~~~~ Bot was started ~~~~~")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)

