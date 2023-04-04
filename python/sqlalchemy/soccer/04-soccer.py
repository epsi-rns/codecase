from sqlalchemy import (
  create_engine, MetaData, Table)
from tabulate import tabulate

str_conn = "sqlite+pysqlite:///./soccer.db"
engine   = create_engine(str_conn)

metadata = MetaData()
metadata.reflect(bind=engine)

people = Table('People', metadata, autoload=True)

with engine.connect() as conn:
  stmt = people.select().where(people.c.id == 7)
  result = conn.execute(stmt)

  row = result.fetchall()
  print(row)

  ks  = result.keys() 
  print(tabulate(row, headers=ks, 
    tablefmt='rounded_outline'))

