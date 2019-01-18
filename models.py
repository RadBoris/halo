from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.ext.declarative import ConcreteBase
from sqlalchemy import and_, or_, not_

class User(Base):
  __tablename__ = 'users'
  uid = Column(Integer, primary_key = True)
  firstname = Column(String(100))
  lastname = Column(String(100))
  email = Column(String(120), unique=True)
  pwdhash = Column(String(54))

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Info(Base):
  __tablename__ = 'info'
  id = Column(Integer, primary_key = True)
  key = Column(String(50))
  value = Column(String(50))
  user_id = Column(Integer, ForeignKey('users.uid'))

  def __init__(self, key, value, user_id):
    self.key = key
    self.value = value
    self.user_id = user_id

