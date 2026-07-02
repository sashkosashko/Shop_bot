from database import db_session
from database.users import User
from database.orders import Order
from database.categories import Category
from database.items import Item

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

async def inline_categories():
    session = db_session.create_session()
    categories = InlineKeyboardBuilder()
    for category in session.query(Category):
        categories.add(InlineKeyboardButton(text=category.name, callback_data=f"category{category.cid}"))
    return categories.adjust(3).as_markup()

async def inline_items(category_id):
    session = db_session.create_session()
    items = InlineKeyboardBuilder()
    for item in session.query(Item).filter(Item.category == category_id):
        items.add(InlineKeyboardButton(text=item.name, callback_data=f"item{item.iid}"))
    return items.adjust(3).as_markup()