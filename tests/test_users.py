from app import schemas
from db import client, session

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