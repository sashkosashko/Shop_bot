from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.keyboards.user_inlines import to_main, to_categories
import database.requests as rq

async def inline_categories():
    categories = InlineKeyboardBuilder()
    for category in await rq.return_categories_query():
        categories.add(InlineKeyboardButton(text=category.name, callback_data=f"category{category.cid}"))
    categories.row(to_main)
    return categories.adjust(3).as_markup()

async def inline_items(category_id):
    items = InlineKeyboardBuilder()
    for item in await rq.return_items_query():
        items.add(InlineKeyboardButton(text=item.name, callback_data=f"item{item.iid}"))
    items.adjust(3)

    items.row(to_categories)
    items.row(to_main)
    
    return items.as_markup()