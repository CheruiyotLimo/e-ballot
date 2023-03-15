# Query for all users.
# Pick them randomnly, checking their first choice and assigning it to them and removing from db.
# If not, remove their choice and leave them in the db for a second run.

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
import requests
import Scripts

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/")
def first_round(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Get request to execute first part of balloting. Get all the users, randomize their selection and assign them the centers."""

    # Ensure the user is an admin
    oauth2.verify_admin(current_user)

    # Get all registered users in a list
    # user_list = requests.get("http://127.0.0.1:8000/users/")
    users = db.query(models.Users).filter(models.Users.role == None).all()

    # print(current_user.email)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {id} doesn,t exist")

    # Access user ids from randomizer scripts
    for id in Scripts.randomizer.randomizer():
        user = db.query(models.Users).filter(models.Users.id == id)

        # Check the user's first choice
        user_choice = user.first().choice

        # Query the hospital db for the hospital
        hosp = db.query(models.Hospital).filter(models.Users.id == user_choice)
        if hosp.first().slots >= 1:
            # Update hospital slots
            
            print("Successfully assigned hospital.")
        else:
            # Remove hosp from db if slots
            print("Hospital is out of slots.")
            del_hosp = db.query(models.Hospital).filter(models.Users.id == user_choice).first()
            del_hosp.delete(synchronize_session=False)

    return users
