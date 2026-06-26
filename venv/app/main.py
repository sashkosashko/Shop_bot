import asyncio
import os

from database import db_session

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.handlers import user_router

from dotenv import load_dotenv

async def main():
    db_session.global_init("venv/database/my_base.db")

    load_dotenv()
    bot = Bot(os.getenv("TOKEN"))
    ADMIN_ID=int(os.getenv("ADMIN_ID"))
    dp = Dispatcher()
    dp.include_router(user_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
