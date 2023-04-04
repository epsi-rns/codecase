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
people = Table('People',
  metadata, autoload=True)
resps  = Table('Responsibilities',
  metadata, autoload=True)
staff  = Table('StaffResps',
  metadata, autoload=True)

# build the select statement
# select users with doctor role
stmt = people.select().\
  join(staff, people.c.id == staff.c.person_id).\
  join(resps, resps.c.id == staff.c.resp_id).\
  where(resps.c.name == 'Doctor');

# fetch result
with engine.connect() as conn:
  result = conn.execute(stmt)

  ks = result.keys()
  ra = result.fetchall()

  print(tabulate(ra, headers=ks))
