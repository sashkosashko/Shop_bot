from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database import db_session
from database.users import User
from database.orders import Order
from database.categories import Category
from database.items import Item

import app.keyboards as kb
import app.builders as br

user_router = Router()

class Order(StatesGroup):
    selected_item = State()

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

@user_router.callback_query(F.data == "main_menu")
async def menu(callback: CallbackQuery):
    photo = FSInputFile("venv/images_dir/start.png")
    await callback.message.answer_photo(photo=photo,
                        caption="Вы в главном меню!",
                        reply_markup=kb.main_menu)
    await callback.answer()

@user_router.callback_query(F.data == "feedbacks")
async def callbacks(callback: CallbackQuery):
    await callback.message.answer("{Ваша ссылка на отзывы}")
    await callback.answer()

@user_router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.answer("Выберите желаемую категорию товаров:", reply_markup=await br.inline_categories())
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

@user_router.callback_query(lambda call: "category" in call.data)
async def selected_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.selected_item)
    session = db_session.create_session()
    category_id = int(callback.data.split("category")[1])
    category_name = session.query(Category).filter(Category.cid == category_id).first().name
    
    await state.update_data(category_id=category_id, category_name=category_name)
    await callback.message.answer(f"Выберите товар из выбранной вами категории: {category_name}", reply_markup=await br.inline_items(category_id))
    await callback.answer()

@user_router.callback_query(lambda call: "item" in call.data)
async def selected_item(callback: CallbackQuery, state: FSMContext):
    session = db_session.create_session()

    item_id = int(callback.data.split("item")[1])

    item = session.query(Item).filter(Item.iid == item_id).first()
    item_name = item.name
    item_price = item.price

    item_data = await state.get_data()
    category_name = item_data.get("category_name")

    await state.update_data(item_id=item_id)
    await callback.message.answer(f"Вы выбрали:\nКатегория: {category_name}\nТовар: {item_name}\nСтоимость: {item_price}₽\nКоличество:", 
                                    reply_markup=kb.selected_item)
    await callback.answer()