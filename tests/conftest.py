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

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally: 
        db.close()



@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally: 
            session.close() 
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {"reg_num": "H31/2001/2015", "name": "Fraser", "email": 'fras@students.uonbi.ac.ke', 'password': '12345'}
    res = client.post("/users/", json=user_data)
    
    new_user = res.json()
    print(new_user)
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user