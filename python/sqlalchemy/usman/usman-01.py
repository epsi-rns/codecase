from sqlalchemy import create_engine
from sqlalchemy import text

str_conn = "sqlite+pysqlite:///./usman.db"
engine   = create_engine(str_conn)

with engine.connect() as conn:
  result = conn.execute(text("SELECT * FROM USER"))

  print(result.keys())
  print(result.all())
