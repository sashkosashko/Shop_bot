from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Главное меню")]], resize_keyboard=True)
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог🛒", callback_data="catalog")], 
    [InlineKeyboardButton(text="Отзывы📃", callback_data="feedbacks")],
    [InlineKeyboardButton(text="Профиль🔳", callback_data="profile")]])

async def inline_products():
    prods = InlineKeyboardBuilder()
    for prod in catalog_info:
        prods.add(InlineKeyboardButton(text=prod, callback_data=f"{prod}prod"))
    return prods.as_markup()

async def inline_actions():
    actions = InlineKeyboardBuilder()
    for act in catalog_info["Акции"]:
        actions.add(InlineKeyboardButton(text=act, callback_data=f"action{list(catalog_info['actions'].keys()).index(act)}"))
    return actions.adjust(3).as_markup()

async def inline_gems():
    gems = InlineKeyboardBuilder()
    for gem in catalog_info["Гемы"]:
        gems.add(InlineKeyboardButton(text=gem, callback_data=f"{gem}gems"))
    return gems.adjust(3).as_markup()

async def inline_bps():
    bps = InlineKeyboardBuilder()
    for bp in catalog_info["Brawl Pass"]:
        bps.add(InlineKeyboardButton(text=bp, callback_data=f"{bp}bp"))
    return bps.adjust(2).as_markup()