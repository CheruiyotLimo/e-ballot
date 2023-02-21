from fastapi import FastAPI, Depends
from .db import get_db
from sqlalchemy.orm import Session
import models


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "The pathway to your internship future."}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    print(users)
    return users