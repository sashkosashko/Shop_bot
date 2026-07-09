from database import db_session
from database.categories import Category
from database.items import Item
from database.orders import Order
from database.users import User

async def create_user(user_id, name):
    session = db_session.create_session()
    user = User(uid=user_id, name=name, count_of_orders=0, payment_score=0)
    session.add(user)
    session.commit()
    session.close()

async def create_item():
    session = db_session.create_session()

async def create_category():
    session = db_session.create_session()

async def create_order():
    session = db_session.create_session()

async def return_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.uid == user_id).first()
    return user

async def return_item():
    session = db_session.create_session()

async def return_category():
    session = db_session.create_session()

async def return_order():
    session = db_session.create_session()