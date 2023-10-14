import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import date

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    new_actor = (Actor(
        name = 'Shahruk',
        gender = 'Male',
        age = 49
        ))

    new_movie = (Movie(
        title = 'DDLJ',
        release_date = date.today()
        ))

    new_actor.insert()
    new_movie.insert()
    db.session.commit()
'''
Movie
Have title and release date
'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(db.Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    }
  
  def insert(self) :
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()



'''
Actor
Have name, age and gender
'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }
  
  def insert(self) :
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
