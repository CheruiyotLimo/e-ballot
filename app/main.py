from fastapi import FastAPI, Depends, HTTPException, status
from .db import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "The pathway to your internship future."}

@app.get("/users/{id}", response_model=schemas.UserReturn)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {id} doesn,t exist")
    print(user)
    return user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def register_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    user_email = db.query(models.Users).filter(models.Users.email == data.email)
    user_reg_no = db.query(models.Users).filter(models.Users.reg_num == data.reg_num)

    if user_email.first() or user_reg_no.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user already exists with similar email or registration number!!")
    
    data = models.Users(**data.dict())

    db.add(data)
    db.commit()
    db.refresh(data)
    return data
    # return f"the account was succesfully created"