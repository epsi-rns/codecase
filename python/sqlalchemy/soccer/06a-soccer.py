from sqlalchemy import create_engine, text
from tabulate import tabulate
from termcolor import colored

str_conn = "sqlite+pysqlite:///./soccer.db"
engine   = create_engine(str_conn)

with engine.connect() as conn:
  stmt = 'SELECT '\
    + '  People.name, People.age, '\
    + '  People.gender, Seats.name as seat '\
    + 'FROM People '\
    + 'INNER JOIN PlayersSeats '\
    + '  ON People.id = PlayersSeats.person_id '\
    + 'INNER JOIN Roles '\
    + '  ON PlayersSeats.role_id = Roles.id '\
    + 'INNER JOIN Seats '\
    + '  ON PlayersSeats.seat_id = Seats.id; '\

  result = conn.execute(text(stmt))

  ks = result.keys()
  ra = result.all()

  print(colored('PSQL', 'red', attrs=['bold']))
  print(tabulate(ra, headers=ks, tablefmt='psql'))
  print()

