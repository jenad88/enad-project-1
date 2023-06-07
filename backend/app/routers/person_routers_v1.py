from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.db import SessionLocal
from sqlalchemy.orm import Session

import backend.app.models.person_models_v1 as person_models_v1
import backend.app.schemas.person_schemas_v1 as person_schemas_v1

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


router = APIRouter(
    prefix="/v1/persons",
    tags=["persons"],
    responses={404: {"description": "Not found"}},
)

@router.get("", response_model=person_schemas_v1.PersonListResponse, status_code=status.HTTP_200_OK)
def get_persons(session: Session = Depends(get_session)):

    # get all persons
    persons_list = session.query(person_models_v1.Person).all()

    return {"data": persons_list}

@router.post("", response_model=person_schemas_v1.PersonResponse, status_code=status.HTTP_201_CREATED)
def create_person(req: person_schemas_v1.PersonCreate, session: Session = Depends(get_session)):

    # create an instance of the Person database model
    person = person_models_v1.Person(first_name = req.first_name, last_name = req.last_name, active = req.active)

    # add it to the session and commit it
    session.add(person)
    session.commit()
    session.refresh(person)

    return {"data": person}

@router.get("/{id}", response_model=person_schemas_v1.PersonResponse, status_code=status.HTTP_200_OK)
def get_person(id: int, session: Session = Depends(get_session)):

    # get the person item with the given id
    person = session.query(person_models_v1.Person).get(id)

    if not person:
        raise HTTPException(status_code=404, detail=f"person with id: {id} not found")
    
    return {"data": person}

@router.put("/{id}", response_model=person_schemas_v1.PersonResponse, status_code=status.HTTP_200_OK)
def update_person(id: int, req: person_schemas_v1.Person, session: Session = Depends(get_session)):

    # get the person with id
    person = session.query(person_models_v1.Person).get(id)

    # if person with that id was found then update
    if person:
        person.first_name = req.first_name
        person.last_name = req.last_name
        person.active = req.active
        session.commit()

    # check if person exists. If not, raise exception and return 404 not found response
    if not person:
        raise HTTPException(status_code=404, detail=f"person id {id} not found")

    return {"data": person}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(id: int, session: Session = Depends(get_session)):
    session = SessionLocal()

    # get the person with id
    person = session.query(person_models_v1.Person).get(id)

    # if person exists, delete it else raise 404 error
    if person:
        session.delete(person)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"person id {id} not found")

    return None
