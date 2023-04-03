from sqlalchemy import create_engine
from sqlalchemy import text
from tabulate import tabulate
from termcolor import colored

str_conn = "sqlite+pysqlite:///./usman.db"
engine   = create_engine(str_conn)

with engine.connect() as conn:
  stmt = 'SELECT * FROM Admin'
  result = conn.execute(text(stmt))

  ks = result.keys()
  ra = result.all()

  print(colored('PSQL', 'red', attrs=['bold']))
  print(tabulate(ra, headers=ks, tablefmt='psql'))
  print()

