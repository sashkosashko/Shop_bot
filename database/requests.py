from database import db_session
from database.categories import Category
from database.items import Item
from database.orders import Order
from database.users import User
from sqlalchemy import select 


async def create_user(user_id: int, name: str):
    async with db_session.create_session() as session:
        user = User(uid=user_id, name=name, count_of_orders=0, payment_score=0)
        session.add(user)
        await session.commit()

async def create_item(category_id: int, title: str, price: float):
    async with db_session.create_session() as session:
        item = Item(category_id=category_id, title=title, price=price)
        session.add(item)
        await session.commit()

async def create_category(title: str):
    async with db_session.create_session() as session:
        category = Category(title=title)
        session.add(category)
        await session.commit()

async def create_order(user_id: int, item_id: int, status: str):
    async with db_session.create_session() as session:
        order = Order(user_id=user_id, item_id=item_id, status=status)
        session.add(order)
        await session.commit()


async def return_user(user_id: int):
    async with db_session.create_session() as session:
        stmt = select(User).where(User.uid == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def return_item(item_id: int):
    async with db_session.create_session() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def return_category(category_id: int):
    async with db_session.create_session() as session:
        stmt = select(Category).where(Category.id == category_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def return_order(order_id: int):
    async with db_session.create_session() as session:
        stmt = select(Order).where(Order.id == order_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def return_users_query():
    async with db_session.create_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        return result.scalars().all()

async def return_items_query(category_id):
    async with db_session.create_session() as session:
        stmt = select(Item).where(Item.category == category_id)
        result = await session.execute(stmt)
        return result.scalars().all()

async def return_categories_query():
    async with db_session.create_session() as session:
        stmt = select(Category)
        result = await session.execute(stmt)
        return result.scalars().all()

async def return_orders_query():
    async with db_session.create_session() as session:
        stmt = select(Order)
        result = await session.execute(stmt)
        return result.scalars().all()
