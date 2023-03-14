from db import client, session
from app import schemas


# def test_user_login(client):
#     res = client.post("/login", data={"username": "q123@gmail.com", "password": "password12"})
#     print(res.json())
#     assert res.status_code == 200