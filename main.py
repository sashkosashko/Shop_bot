import asyncio
import os
import logging

from database import db_session
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers.user_handlers import user_router
from app.handlers.admin_handlers import admin_router

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("bot.log", encoding="utf-8")
        ]
    )

    load_dotenv()

    await db_session.global_init("database/my_base.db")

    token = os.getenv("TOKEN")
    if not token:
        logging.critical("Токен бота (TOKEN) не найден в файле .env!")
        return

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(admin_router)
    dp.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")