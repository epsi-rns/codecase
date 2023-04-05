from sqlalchemy import create_engine
from sqlalchemy import text

str_conn = "sqlite+pysqlite:///./soccer.db"
engine   = create_engine(str_conn)

with engine.connect() as conn:
  stmt   = "SELECT * FROM People LIMIT 5"
  result = conn.execute(text(stmt))

  ra = result.all()
  for row in ra:
    print(f"id: {row.id}  "\
          f"name: {row.name}  "\
          f"age: {row.age}  "\
          f"gender: {row.gender}")
