from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, select
from tabulate import tabulate

# create a SQLite engine
str_conn = "sqlite+pysqlite:///./usman.db"
engine   = create_engine(str_conn)

# create a SQLAlchemy metadata object
metadata = MetaData()
metadata.reflect(bind=engine)

# reflect the existing tables
users = Table('User', metadata, autoload=True)
roles = Table('Role', metadata, autoload=True)
perms = Table('Permission', metadata, autoload=True)
urps  = Table('User_Role_Permission',
  metadata, autoload=True)

# build the select statement
# select users with admin privileges
stmt = users.select().\
  join(urps, urps.c.user_id == users.c.id).\
  join(roles, roles.c.id == urps.c.role_id).\
  where(roles.c.name == 'admin').\
  group_by(users.c.id)

# fetch result
with engine.connect() as conn:
  result = conn.execute(stmt)

  ks = result.keys()
  ra = result.fetchall()

  print(tabulate(ra, headers=ks))
