from sqlalchemy import Column, Integer, String, Boolean
from backend.app.db import Base

# Define Person class inheriting from Base
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name =  Column(String(50))
    last_name =  Column(String(50))
    active =  Column(Boolean)