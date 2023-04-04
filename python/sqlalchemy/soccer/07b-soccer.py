from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, select
from tabulate import tabulate

# create a SQLite engine
str_conn = "sqlite+pysqlite:///./soccer.db"
engine   = create_engine(str_conn)

# create a SQLAlchemy metadata object
metadata = MetaData()
metadata.reflect(bind=engine)

# reflect the existing tables
people = metadata.tables['People']
resps  = metadata.tables['Responsibilities']
staff  = metadata.tables['StaffResps']

# build inner joins
join_stmt = people
join_stmt = join_stmt.join(staff,
  people.c.id == staff.c.person_id)
join_stmt = join_stmt.join(resps,
  resps.c.id == staff.c.resp_id)

# select users with doctor role
stmt = select(people.c.email, resps.c.name)
stmt = stmt.select_from(join_stmt)
stmt = stmt.where(resps.c.name == 'Doctor');

# fetch result
with engine.connect() as conn:
  result = conn.execute(stmt)

  ks = result.keys()
  ra = result.fetchall()

  print(tabulate(ra, headers=ks))
