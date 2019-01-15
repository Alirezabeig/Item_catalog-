import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__='user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    

# This class will be for collecting the info of the categories
class Category(Base):
    __tablename__='category'

    id= Column(Integer, primary_key=True)
    name= Column(String (30), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,

        }
    #user_id= Column(Integer,ForeignKey('user.id'))

# This class will be for collecting the info of the items of each category
class CategoryItem(Base):
    __tablename__='categoryItem'

    name= Column(String(30), nullable=False)
    id= Column(Integer, primary_key=True)
    category_id = Column(Integer,ForeignKey('category.id'))
    category= relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,

        }
# added this serialize function to be able to send JSON objects in a serializable format


engine = create_engine('sqlite:///CategoryUsers.db')


Base.metadata.create_all(engine)
