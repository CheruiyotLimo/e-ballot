from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/", status_code=status.HTTP_200_OK)
def user_login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Query for user with specified email
    user = db.query(models.Users).filter(models.Users.email==user_credential.username).first()

    # Raise exception if user is not found
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with email {user_credential.username} not found")
    
    # Verify the specified password to be correct
    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong password")
    
    # To implement: generation of a new token.
    access_token = oauth2.create_access_token({"user_id": user.id, "reg_num": user.reg_num})


    # Return success message
    print(user.name)
    return {"access_token": access_token, "token_type": "bearer"}

