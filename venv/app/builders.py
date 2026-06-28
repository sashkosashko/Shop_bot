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