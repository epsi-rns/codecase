from sqlalchemy import (
  create_engine, ForeignKey, 
  Table, Column, Integer, String)
from sqlalchemy.orm import (
  sessionmaker, relationship, DeclarativeBase)

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
    roles = relationship('Role',
      secondary='User_Role_Permission')

class Role(Base):
    __tablename__ = 'Role'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    permissions = relationship('Permission',
      secondary='Role_Permission')

class Permission(Base):
    __tablename__ = 'Permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class User_Role_Permission(Base):
    __tablename__ = 'User_Role_Permission'

    user_id = Column(Integer,
      ForeignKey('User.id'), primary_key=True)
    role_id = Column(Integer,
      ForeignKey('Role.id'), primary_key=True)
    permission_id = Column(Integer,
      ForeignKey('Permission.id'), primary_key=True)

class Role_Permission(Base):
    __tablename__ = 'Role_Permission'

    role_id = Column(Integer,
      ForeignKey('Role.id'), primary_key=True)
    permission_id = Column(Integer,
      ForeignKey('Permission.id'), primary_key=True)

# Initialization
str_conn = "sqlite+pysqlite:///./usman.db"
engine   = create_engine(str_conn)

Session = sessionmaker(bind=engine)
session = Session()

keys = User.metadata.tables['User'].columns.keys()

user_row = lambda u :\
  (u.id, u.username, u.password, u.email)

# Example Case
admins = session.query(User)\
  .join(User_Role_Permission)\
  .join(Role)\
  .filter_by(name='admin')\
  .all()

rows = [user_row(u) for u in admins]
print(tabulate(rows, headers=keys, tablefmt='psql'))
