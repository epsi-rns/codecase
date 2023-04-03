from sqlalchemy import create_engine
from sqlalchemy import text
from tabulate import tabulate
from termcolor import colored

str_conn = "sqlite+pysqlite:///./usman.db"
engine   = create_engine(str_conn)

with engine.connect() as conn:
  stmt = 'SELECT User.* FROM User '\
    + 'INNER JOIN User_Role_Permission ON User_Role_Permission.user_id = User.id '\
    + 'INNER JOIN Role ON Role.id = User_Role_Permission.role_id '\
    + 'WHERE Role.name = "admin" '\
    + 'GROUP BY User.id'
  result = conn.execute(text(stmt))

  ks = result.keys()
  ra = result.all()

  print(colored('PSQL', 'red', attrs=['bold']))
  print(tabulate(ra, headers=ks, tablefmt='psql'))
  print()

