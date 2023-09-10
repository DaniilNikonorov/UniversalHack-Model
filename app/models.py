from .database import Base

from sqlalchemy import String, Date, Integer, Column, Numeric
from clickhouse_sqlalchemy import engines


# Предсказания офлайн
class Prediction(Base):
    __tablename__ = 'val_predictions'

    Column1 = Column('Column1', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    item_id = Column('item_id', Integer)
    rank_ctb = Column('rank_ctb', Integer)

    __table_args__ = (
        engines.Memory(),
    )


# Вот это под товары, поменять таблицу на товары
class UserInfo(Base):
    __tablename__ = 'val_dataset'

    Column1 = Column('Column1', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    device_id = Column('device_id', Integer)
    item_id = Column('item_id', Integer)
    server_date = Column('server_date', String)
    local_date = Column('local_date', String)
    name = Column('name', String)
    price = Column('price', Numeric)
    quantity = Column('quantity', Numeric)
    my_ckecker = Column('my_ckecker', String)

    __table_args__ = (
        engines.Memory(),
    )


class Items(Base):
    __tablename__ = 'items_supermarket'

    Column1 = Column('Column1', Integer, primary_key=True)
    item_id = Column('item_id', Integer)
    name = Column('name', String)

    __table_args__ = (
        engines.Memory(),
    )


class Points(Base):
    __tablename__ = 'supermarket_train'

    Column1 = Column('Column1', Integer, primary_key=True)
    device_id = Column('device_id', Integer)
    receipt_id = Column('receipt_id', Integer)
    item_id = Column('item_id', Integer)
    server_date = Column('server_date', String)
    local_date = Column('local_date', String)
    name = Column('name', String)
    price = Column('price', Numeric)
    quantity = Column('quantity', Numeric)
    my_ckecker = Column('my_ckecker', String)

    __table_args__ = (
        engines.Memory(),
    )
