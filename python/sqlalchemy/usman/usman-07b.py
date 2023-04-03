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
users = metadata.tables['User']
roles = metadata.tables['Role']
perms = metadata.tables['Permission']
urps  = metadata.tables['User_Role_Permission']

# build inner joins
join_stmt = users
join_stmt = join_stmt.join(urps,
  urps.c.user_id == users.c.id)
join_stmt = join_stmt.join(roles,
  roles.c.id == urps.c.role_id)

# select users with admin privileges
stmt = select(users.c.username, users.c.email)
stmt = stmt.select_from(join_stmt)
stmt = stmt.where(roles.c.name == 'admin')
stmt = stmt.group_by(users.c.id)

# fetch result
with engine.connect() as conn:
  result = conn.execute(stmt)

  ks = result.keys()
  ra = result.fetchall()

  print(tabulate(ra, headers=ks))
