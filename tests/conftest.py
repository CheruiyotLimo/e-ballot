from fastapi.testclient import TestClient
from app.main import app
from app import main, schemas, oauth2
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

@pytest.fixture
def token(test_user):
    token = oauth2.create_access_token(user_data={'user_id': test_user['id'], 'reg_num': test_user['reg_num']})
    return token

@pytest.fixture
def test_user_admin(client):
    user_data = {"reg_num": settings.admin_reg, "name": "Mimo", "email": 'mims@students.uonbi.ac.ke', 'password': '56789'}
    res = client.post("/users/", json=user_data)
    
    new_user = res.json()
    print(new_user)
    new_user['password'] = user_data['password']
    new_user['role'] = 'admin'
    assert res.status_code == 201
    return new_user

@pytest.fixture
def token_admin(test_user_admin):
    token = oauth2.create_access_token(user_data={'user_id': test_user_admin['id'], 'reg_num': test_user_admin['reg_num']})
    return token


@pytest.fixture
def authorized_client(token, client):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client

@pytest.fixture
def authorized_client_admin(token_admin, client):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token_admin}'
    }
    return client

