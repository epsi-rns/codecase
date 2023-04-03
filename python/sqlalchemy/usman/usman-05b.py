from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from tabulate import tabulate
from termcolor import colored

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

user_row = lambda u :\
  (u.id, u.username, u.password, u.email)

# Case 1
print(colored('case 1', 'red', attrs=['bold']))
user = session.query(User).filter_by(id=3).first()
row = user_row(user)
print(tabulate([row], headers=keys, tablefmt='psql'))
print()

# Case 2
print(colored('case 2', 'green', attrs=['bold']))
all_users = session.query(User).all()
rows = [user_row(u) for u in all_users]
print(tabulate(rows, headers=keys, tablefmt='psql'))
print()

# Case 3
print(colored('case 3', 'blue', attrs=['bold']))
users_with_email = session.query(User)\
  .filter_by(email='bob@example.com').all()
rows = [user_row(u) for u in users_with_email]
print(tabulate(rows, headers=keys, tablefmt='psql'))
print()
