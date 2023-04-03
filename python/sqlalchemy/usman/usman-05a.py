from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from tabulate import tabulate

# Class Definition
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

# Initialization
str_conn = "sqlite+pysqlite:///./usman.db"
engine   = create_engine(str_conn)

Session = sessionmaker(bind=engine)
session = Session()

keys = User.metadata.tables['User'].columns.keys()

result = session.query(User).all()
rows = [
  (r.id, r.username, r.password, r.email)
  for r in result]

print(tabulate(rows, headers=keys, tablefmt='psql'))
