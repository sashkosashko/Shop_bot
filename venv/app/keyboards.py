from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Главное меню")]], resize_keyboard=True)
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог📃", callback_data="catalog")], 
    [InlineKeyboardButton(text="Корзина🛒", callback_data="feedbacks")],
    [InlineKeyboardButton(text="Профиль😎", callback_data="profile")],
    [InlineKeyboardButton(text="Отзывы🖊", callback_data="feedbacks")]])
profile_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="История заказов🛒", callback_data="history_od_orders")], 
    [InlineKeyboardButton(text="В главное меню📃", callback_data="main_menu")]])