import logging
import os
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

import app.keyboards.admin_builders as br
import app.keyboards.admin_inlines as il

import database.requests as rq

admin_router = Router()

ADMIN_SET = set(os.getenv("ADMIN_ID", "").split(","))
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

@admin_router.message(F.text == ADMIN_PASSWORD)
async def admin_menu(message: Message):
    if str(message.from_user.id) in ADMIN_SET:
        await message.answer("Авторизация успешна! Что хотите сделать?")