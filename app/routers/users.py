from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
# from ...Scripts import scripts


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{id}", response_model=schemas.UserReturn)
def get_users(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    print(current_user.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {id} doesn,t exist")
    print(user)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def register_user(data: schemas.UserCreate, db: Session = Depends(get_db)):

    # Verify it is a valid email address
    # if not scripts.email_verifier(data.email):
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The email provided is not a valid email address")

    user_email = db.query(models.Users).filter(models.Users.email == data.email)
    user_reg_no = db.query(models.Users).filter(models.Users.reg_num == data.reg_num)

    if user_email.first() or user_reg_no.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user already exists with similar email or registration number!!")
    
    new_password = utils.hash(data.password)
    data.password = new_password
    data = models.Users(**data.dict())

    db.add(data)
    db.commit()
    db.refresh(data)
    return data