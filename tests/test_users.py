from fastapi.testclient import TestClient
from app import main, schemas

client = TestClient(main.app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.status_code == 200

def test_add_user():
    res = client.post("/users/", json={"reg_num": "H31/2000/1298", "name": "Fraser", "email": "q123@gmail.com", "password": "password123"})
    test_user = schemas.UserReturn(**res.json())
    assert test_user.email == "q123@gmail.com"
    assert res.status_code == 201