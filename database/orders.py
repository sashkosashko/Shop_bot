import sqlalchemy
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__= "orders"

    oid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer)
    item = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)