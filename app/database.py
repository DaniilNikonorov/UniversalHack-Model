from sqlalchemy import create_engine, MetaData
from clickhouse_sqlalchemy import make_session, get_declarative_base

db_url = 'clickhouse://danya:qwerty@94.139.255.66:8123/default'
engine = create_engine(db_url)

session = make_session(engine)
metadata = MetaData(bind=engine)

Base = get_declarative_base(metadata=metadata)
