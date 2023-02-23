from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils


router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/", status_code=status.HTTP_200_OK)
def user_login(user_credential: schemas.UserLogin, db: Session = Depends(get_db)):
    
    # Query for user with sspecified email
    user = db.query(models.Users).filter(models.Users.email==user_credential.username).first()

    # Raise exception if user is not found
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with email {user_credential.username} not found")
    
    # Verify the specified password to be correct
    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong password")
    
    # To implement: generation of a new token.

    # Return success message
    print(user.name)
    return "Successfully logged in."