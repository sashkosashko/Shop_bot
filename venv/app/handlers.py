from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from database import db_session
from database.users import User
from database.orders import Order
from database.categories import Category
from database.items import Item

import app.keyboards as kb

user_router = Router()

@user_router.message(CommandStart())
async def start(message: Message):
    session = db_session.create_session()
    user_id = message.from_user.id
    if not session.query(User).filter(User.uid == user_id).first():
        user = User(uid=user_id, count_of_orders=0)
        session.add(user)
        await message.delete()
        await message.answer("😀")
        photo = FSInputFile("venv/images_dir/start.png")
        await message.answer_photo(photo=photo,
                            caption="Привет, пользователь! Ты попал в наш магазинчик {название} впервые. {желаемое описание}",
                            reply_markup=kb.main_menu)
    else:
        await message.delete()
        await message.answer("😀")
        photo = FSInputFile("venv/images_dir/start.png")
        await message.answer_photo(photo=photo,
                            caption="Ого, вы вернулись! Добро пожаловать в магазин {название}",
                            reply_markup=kb.main_menu)
    session.commit()
    session.close()

@user_router.message(F.text == "Главное меню")
async def menu(message: Message):
    photo = FSInputFile("venv/images_dir/start.png")
    await message.reply_photo(photo=photo,
                        caption="Вы в главном меню!",
                        reply_markup=kb.main_menu)

@user_router.callback_query(F.data == "feedbacks")
async def callbacks(callback: CallbackQuery):
    await callback.message.answer("{Ваша ссылка на отзывы}")
    await callback.answer()

@user_router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.answer("Выберите желаемый товар", reply_markup=await kb.inline_products())
    await callback.answer()

@user_router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    session = db_session.create_session()
    user_id = callback.from_user.id
    name = callback.from_user.first_name
    user = session.query(User).filter(User.uid == user_id).first()
    count_of_orders = user.count_of_orders
    photo = FSInputFile("venv/images_dir/start.png")
    await callback.message.answer_photo(photo=photo,
                                    caption=f"Ваш профиль:\nИмя: {name}\nКоличество заказов: {count_of_orders}",
                                    reply_markup=kb.profile_menu)
    await callback.answer()
    session.close()

async def inline_products():
    pass