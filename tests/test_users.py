from fastapi.testclient import TestClient
from app.main import app
from app import main, schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.db import get_db, Base


db_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(db_url) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally: 
        db.close() 


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



def test_root():
    res = client.get("/")
    print(res.json())
    assert res.status_code == 200

def test_register_user():
    res = client.post("/users/", json={"reg_num": "H31/200/1298", "name": "Fraser", "email": "q123@gmail.com", "password": "password12"})
    print(res.json())
    test_user = schemas.UserReturn(**res.json())
    
    assert test_user.email == "q123@gmail.com"
    assert res.status_code == 201