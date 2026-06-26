from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Главное меню")]], resize_keyboard=True)
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог🛒", callback_data="catalog")], 
    [InlineKeyboardButton(text="Отзывы📃", callback_data="feedbacks")],
    [InlineKeyboardButton(text="Профиль🔳", callback_data="profile")]])
profile_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="История заказов🛒", callback_data="history_od_orders")], 
    [InlineKeyboardButton(text="В главное меню📃", callback_data="main_menu")]])

async def inline_products():
    pass