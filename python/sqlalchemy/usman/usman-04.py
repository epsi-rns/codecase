from sqlalchemy import create_engine, MetaData, Table
from tabulate import tabulate

str_conn = "sqlite+pysqlite:///./usman.db"
engine   = create_engine(str_conn)

metadata = MetaData()
metadata.reflect(bind=engine)

users = Table('User', metadata, autoload=True)

with engine.connect() as conn:
  stmt = users.select().where(users.c.id == 1)
  result = conn.execute(stmt)

  row = result.fetchall()
  print(row)

  ks  = result.keys() 
  print(tabulate(row, headers=ks, 
    tablefmt='rounded_outline'))

