from sqlalchemy import (
  create_engine, Table, Column, Integer, String)
from sqlalchemy.orm import (
  sessionmaker, DeclarativeBase)

from tabulate import tabulate

# Class Definition
class Base(DeclarativeBase):
  pass

class People(Base):
  __tablename__ = 'People'

  id = Column(Integer, primary_key=True)
  name = Column(String(255), nullable=False)
  email = Column(String(100), nullable=False)
  age = Column(Integer)
  gender = Column(String(50))

# Initialization
str_conn = "sqlite+pysqlite:///./soccer.db"
engine   = create_engine(str_conn)

Session = sessionmaker(bind=engine)
session = Session()

keys = People.metadata\
  .tables['People'].columns.keys()

# Running Query
result = session.query(People).all()
rows = [
  (p.id, p.name, p.email, p.age, p.gender)
  for p in result]

print(tabulate(rows, headers=keys,
  tablefmt='psql'))
