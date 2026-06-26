import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__= "users"

    uid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    count_of_orders = sqlalchemy.Column(sqlalchemy.Integer)