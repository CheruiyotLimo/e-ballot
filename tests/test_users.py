from app import schemas
from jose import jwt
# from db import client, session
from app.config import settings
import pytest

@pytest.fixture()
def test_user(client):
    user_data = {"reg_num": "H31/2001/2015", "name": "Fraser", "email": 'fras@students.uonbi.ac.ke', 'password': '12345'}
    res = client.post("/users/", json=user_data)
    
    new_user = res.json()
    print(new_user)
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.status_code == 200

def test_register_user(client):
    res = client.post("/users/", json={"reg_num": "H31/200/1298", "name": "Fraser", "email": "q123@students.uonbi.ac.ke", "password": "password12"})
    print(res.json())
    test_user = schemas.UserReturn(**res.json())
    
    assert test_user.email == "q123@students.uonbi.ac.ke"
    assert res.status_code == 201

def test_user_login(client, test_user):
    res = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload.get("user_id")
    assert user_id == int(test_user['id'])
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

