import logging
import os
from aiogram import F, Router
from filters.chat_types import IsAdmin
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

import app.keyboards.admin_builders as br
import app.keyboards.admin_inlines as il

import database.requests as rq

class AddAdminState(StatesGroup):
    waiting_for_id = State()

admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

@admin_router.message(F.text == ADMIN_PASSWORD)
async def admin_menu(message: Message):
    await message.answer("Вы вошли как админ. Что хотите сделать?", reply_markup=il.admin_menu)