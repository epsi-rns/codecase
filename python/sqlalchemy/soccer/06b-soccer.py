from sqlalchemy import create_engine, text
from tabulate import tabulate

str_conn = "sqlite+pysqlite:///./soccer.db"
engine   = create_engine(str_conn)

with engine.connect() as conn:
  stmt = 'SELECT name, age, gender, seat '\
       + 'FROM Players'
  result = conn.execute(text(stmt))

  ks = result.keys()
  ra = result.all()

  print(tabulate(ra, headers=ks, tablefmt='psql'))


