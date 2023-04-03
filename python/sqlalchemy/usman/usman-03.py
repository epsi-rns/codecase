from sqlalchemy import create_engine
from sqlalchemy import text
from tabulate import tabulate
from termcolor import colored

str_conn = "sqlite+pysqlite:///./usman.db"
engine   = create_engine(str_conn)

with engine.connect() as conn:
  stmt   = "SELECT * FROM USER"
  result = conn.execute(text(stmt))

  ks = result.keys()
  ra = result.all()

  print(colored('PSQL', 'red', attrs=['bold']))
  print(tabulate(ra, headers=ks, tablefmt='psql'))
  print()

  print(colored('Github', 'green', attrs=['bold']))
  print(tabulate(ra, headers=ks, tablefmt='github'))
  print()

  print(colored('Rounded Outline', 'blue',
    attrs=['bold']))
  print(tabulate(ra, headers=ks, 
    tablefmt='rounded_outline'))
  print()
