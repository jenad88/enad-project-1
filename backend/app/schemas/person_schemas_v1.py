from typing import List
from pydantic import BaseModel

# Create Person Schema
class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    active: bool

# Create Person Base Model
class Person(BaseModel):
    id: int
    first_name: str
    last_name: str
    active: bool

    class Config:
        orm_mode = True

class PersonResponse(BaseModel):
    data: Person

class PersonListResponse(BaseModel):
    data: List[Person]