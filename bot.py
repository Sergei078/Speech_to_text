import asyncio
from aiogram import Dispatcher
from handlers import router
import logging
from dotenv import load_dotenv
from bot_token import bot

load_dotenv()

dp = Dispatcher()


async def start_bot():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start_bot())
    except Exception as e:
        logging.error(str(e))
