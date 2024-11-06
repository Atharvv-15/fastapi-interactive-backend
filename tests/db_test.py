import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from app.db import Base,get_db
from app import models

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0142@localhost:5432/fastapi-DB-test"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# override the get_db dependency, so that the test database is used, instead of the development database, when testing
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # drop all tables, then create all tables, then yield the test client, this way the test database is 
    # reset to a clean state before each test, and get to know the current state of the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 
    yield TestClient(app)