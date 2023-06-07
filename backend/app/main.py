from fastapi import FastAPI
from backend.app.routers import person_routers_v1
from backend.app.db import Base, engine

def create_app():
    app = FastAPI()

    app.include_router(person_routers_v1.router, prefix="/api")

    return app

# Create the database
Base.metadata.create_all(engine)

app = create_app()