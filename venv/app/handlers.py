from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

user_router = Router()
users = set()

@user_router.message(CommandStart())
async def start(message: Message):
    users.add(message.from_user.id)
    await message.delete()
    await message.answer("😀")
    photo = FSInputFile("images_dir/start.png")
    await message.answer_photo(photo=photo,
                        caption="Привет, пользователь! Ты попал в наш магазинчик {название}. {желаемое описание}", reply_markup=kb.main_menu)

@user_router.message(F.text == "Главное меню")
async def menu(message: Message):
    photo = FSInputFile("images_dir/start.png")
    await message.reply_photo(photo=photo,
                        caption="Привет, пользователь! Ты попал в наш магазинчик {название}. {желаемое описание}", reply_markup=kb.main_menu)

@user_router.callback_query(F.data == "feedbacks")
async def callbacks(callback: CallbackQuery):
    await callback.message.answer("{Ваша ссылка на отзывы}")
    await callback.answer()

@user_router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.answer("Выберите желаемый товар", reply_markup=await kb.inline_products())
    await callback.answer()

@user_router.callback_query(lambda call: "Гемы" in call.data and "prod" in call.data)
async def gems(callback: CallbackQuery):
    await callback.message.answer("Выберите количество гемов:", reply_markup=await kb.inline_gems())
    await callback.answer()

@user_router.callback_query(lambda call: "gems" in call.data)
async def selected_gems(callback_query: CallbackQuery):
    amount_gems = callback_query.data[:-4]
    await callback_query.message.answer(f"Вы выбрали {amount_gems} гемов. Ссылка на оплату:")
    await callback_query.answer()

@user_router.callback_query(lambda call: "Brawl Pass" in call.data and "prod" in call.data)
async def bps(callback: CallbackQuery):
    await callback.message.answer("Выберите Brawl Pass:", reply_markup=await kb.inline_bps())
    await callback.answer()

@user_router.callback_query(lambda call: "bp" in call.data)
async def selected_bp(callback_query: CallbackQuery):
    type_bp = callback_query.data[:-2]
    await callback_query.message.answer(f"Вы выбрали {type_bp}. Ссылка на оплату:")
    await callback_query.answer()

@user_router.callback_query(lambda call: "Pro Pass" in call.data and "prod" in call.data)
async def pp(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали Pro Pass. Ссылка на оплату:")
    await callback.answer()

@user_router.callback_query(lambda call: "Акции" in call.data and "prod" in call.data)
async def actions(callback: CallbackQuery):
    await callback.message.answer("Выберите акцию:", reply_markup=await kb.inline_actions())
    await callback.answer()