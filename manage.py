from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from database import Base
from sqlalchemy import Column, Integer, String

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ubzdjahonslgwk:4516f846862bbb569079f2b53bcccd8a145315c17098df6390746eee91fd9995@ec2-184-72-230-93.compute-1.amazonaws.com:5432/daco986o48khus'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

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

if __name__ == '__main__':
    manager.run()
