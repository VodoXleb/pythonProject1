import asyncio
import logging
import sys
from aiogram import Bot
from aiogram.enums import ParseMode

from handlers import cmd_start_handler, write_help, manage_task
from loader import dp, msg_router, callback_router
from loader import TOKEN


async def main() -> None:
    dp.include_router(msg_router)
    dp.include_router(callback_router)
    msg_router.message.register(cmd_start_handler)
    callback_router.message.register(cmd_start_handler)
    msg_router.message.register(write_help)
    msg_router.message.register(manage_task)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

