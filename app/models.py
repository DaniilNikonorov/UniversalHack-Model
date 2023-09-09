from .database import Base

from sqlalchemy import String, Date, Integer, Column, Numeric
from clickhouse_sqlalchemy import engines


# Вот это под косметику, поменять таблицу на косметику
class Cosmetic(Base):
    __tablename__ = 'preds_dataset'

    Column1 = Column('Column1', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    item_id = Column('item_id', Integer)
    rank = Column('rank', Integer)
    ctb_pred = Column('ctb_pred', Numeric)
    rank_ctb = Column('rank_ctb', Integer)

    __table_args__ = (
        engines.Memory(), {'extend_existing': True}
    )

    # TODO: выпилить, когда появятся нормальные таблицы
    __mapper_args__ = {
        "polymorphic_identity": "cosmetic",
    }


# Вот это под товары, поменять таблицу на товары
class Market(Base):
    __tablename__ = 'preds_dataset'

    Column1 = Column('Column1', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    item_id = Column('item_id', Integer)
    rank = Column('rank', Integer)
    ctb_pred = Column('ctb_pred', Numeric)
    rank_ctb = Column('rank_ctb', Integer)

    __table_args__ = (
        engines.Memory(), {'extend_existing': True}
    )

    # TODO: выпилить, когда появятся нормальные таблицы
    __mapper_args__ = {
        "polymorphic_identity": "market",
    }


class Items(Base):
    __tablename__ = 'items_supermarket'

    Column1 = Column('Column1', Integer, primary_key=True)
    item_id = Column('item_id', Integer)
    name = Column('name', String)

    __table_args__ = (
        engines.Memory()
    )


class Points(Base):
    __tablename__ = 'supermarket_train'

    Column1 = Column('Column1', Integer, primary_key=True)
    device_id = Column('device_id', Integer)
    receipt_id = Column('receipt_id', Integer)
    item_id = Column('item_id', Integer)
    server_date = Column('server_date', Integer)
    local_date = Column('local_date', Integer)
    name = Column('name', Integer)
    price = Column('price', Integer)
    quantity = Column('quantity', Integer)
    my_ckecker = Column('my_ckecker', Integer)

    __table_args__ = (
        engines.Memory()
    )
