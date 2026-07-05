from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог📃", callback_data="catalog")], 

    [InlineKeyboardButton(text="Корзина🛒", callback_data="basket")],

    [InlineKeyboardButton(text="Профиль😎", callback_data="profile")],

    [InlineKeyboardButton(text="Отзывы🖊", callback_data="feedbacks")]])

to_main = InlineKeyboardButton(text="В главное меню📃", callback_data="main_menu")

profile_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="История заказов🛒", callback_data="history_od_orders")], 
    
    [to_main]])


selected_item = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Увеличить количество⬆", callback_data="plus_amount"), 
    InlineKeyboardButton(text="Уменьшить количество⬇", callback_data="minus_amount")],

    [InlineKeyboardButton(text="Купить🎁", callback_data="buy_item")],

    [InlineKeyboardButton(text="Положить в корзину🛒", callback_data="put_into_basket")],
    
    [to_main]])