from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

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

class Role(Base):
    __tablename__ = 'Roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Responsibility(Base):
    __tablename__ = 'Responsibilities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Seat(Base):
    __tablename__ = 'Seats'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class PeopleRoles(Base):
    __tablename__ = 'PeopleRoles'

    person_id = Column(Integer, ForeignKey('People.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('Roles.id'), primary_key=True)

    person = relationship(People, backref='roles')
    role = relationship(Role, backref='people')

class PlayersSeats(Base):
    __tablename__ = 'PlayersSeats'

    person_id = Column(Integer, ForeignKey('People.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('Roles.id'), primary_key=True)
    seat_id = Column(Integer, ForeignKey('Seats.id'), primary_key=True)
    is_bench = Column(Boolean, default=False)

    person = relationship(People, backref='player_seats')
    role = relationship(Role, backref='players')
    seat = relationship(Seat, backref='players')

class StaffResps(Base):
    __tablename__ = 'StaffResps'

    person_id = Column(Integer, ForeignKey('People.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('Roles.id'), primary_key=True)
    resp_id = Column(Integer, ForeignKey('Responsibilities.id'), primary_key=True)

    person = relationship(People, backref='staff_responsibilities')
    role = relationship(Role, backref='staff')
    responsibility = relationship(Responsibility, backref='staff')
