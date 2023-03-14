from fastapi.testclient import TestClient
from app.main import app
from app import main, schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.db import get_db, Base
import pytest


db_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(db_url) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





# client = TestClient(app)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally: 
        db.close()



@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally: 
            session.close() 
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    

def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.status_code == 200

def test_register_user(client):
    res = client.post("/users/", json={"reg_num": "H31/200/1298", "name": "Fraser", "email": "q123@gmail.com", "password": "password12"})
    print(res.json())
    test_user = schemas.UserReturn(**res.json())
    
    assert test_user.email == "q123@gmail.com"
    assert res.status_code == 201