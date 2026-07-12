import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__= "users"

    uid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    count_of_orders = sqlalchemy.Column(sqlalchemy.Integer)
    payment_score = sqlalchemy.Column(sqlalchemy.Integer)