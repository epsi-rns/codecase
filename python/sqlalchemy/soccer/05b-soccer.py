from sqlalchemy import (
  create_engine, Table, Column, Integer, String)
from sqlalchemy.orm import (
  sessionmaker, DeclarativeBase)

from tabulate import tabulate
from termcolor import colored

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

person_row = lambda p : (\
  p.id, p.name, p.email, p.age, p.gender)

# Case 1
print(colored('case 1', 'red', attrs=['bold']))
person = session.query(People).filter_by(id=8)\
 .first()

row = person_row(person)
print(tabulate([row], headers=keys,
  tablefmt='psql'))
print()

# Case 2
print(colored('case 2', 'green', attrs=['bold']))
all_persons = session.query(People)\
  .limit(7).all()

rows = [person_row(u) for u in all_persons]
print(tabulate(rows, headers=keys,
  tablefmt='psql'))
print()

# Case 3
print(colored('case 3', 'blue', attrs=['bold']))
persons_with_email = session.query(People)\
  .filter_by(email='coach.smith@example.com')\
  .all()

rows = [person_row(u) for u in persons_with_email]
print(tabulate(rows, headers=keys,
  tablefmt='psql'))
print()
