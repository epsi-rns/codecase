from sqlalchemy import (
  create_engine, ForeignKey, 
  Table, Column, Integer, String)
from sqlalchemy.orm import (
  sessionmaker, relationship, DeclarativeBase)

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

class Resp(Base):
  __tablename__ = 'Responsibilities'

  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)

class StaffResps(Base):
  __tablename__ = 'StaffResps'

  person_id = Column(Integer,
    ForeignKey('People.id'), primary_key=True)
  resp_id = Column(Integer,
    ForeignKey('Responsibilities.id'),
    primary_key=True)

# Initialization
str_conn = "sqlite+pysqlite:///./soccer.db"
engine   = create_engine(str_conn)

Session = sessionmaker(bind=engine)
session = Session()

keys = People.metadata\
  .tables['People'].columns.keys()

person_row = lambda p : (\
  p.id, p.name, p.email, p.age, p.gender)

# Example Case
# select people with doctor role
doctors = session.query(People)\
  .join(StaffResps)\
  .join(Resp)\
  .filter_by(name='Doctor')\
  .all()

rows = [person_row(u) for u in doctors]
print(tabulate(rows, headers=keys))

