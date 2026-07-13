from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пользователи👤", callback_data="users")], 

    [InlineKeyboardButton(text="Каталог🛒", callback_data="catalog")],

    [InlineKeyboardButton(text="Заказы📦", callback_data="orders")]])