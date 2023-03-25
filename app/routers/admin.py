# Query for all users.
# Pick them randomnly, checking their first choice and assigning it to them and removing from db.
# If not, remove their choice and leave them in the db for a second run.

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
import requests
from Scripts import randomizer
from . import hosp, users, auth

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/", status_code=status.HTTP_201_CREATED)
def first_round(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Get request to execute first part of balloting. Get all the users, randomize their selection and assign them the centers."""

    # Ensure the user is an admin
    oauth2.verify_admin(current_user)

    # Get all registered users in a list
    user_list = users.get_users(db=db, current_user=current_user)

    # print(current_user.email)
    if not user_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No registered users exist")

    # Access user ids from randomizer scripts
    for id in randomizer.randomizer():
        user = db.query(models.Users).filter(models.Users.id == id)

        print(id)
        if not user.first():
            continue
        # Check the user's first choice
        user_choice = user.first().choice
        print(user_choice)

        # Query the hospital db for the hospital
        hosp = db.query(models.Hospital).filter(models.Hospital.id == user_choice)

        if hosp.first().slots >= 1:

            # Update hospital slots
            hosp.update({"slots": (hosp.first().slots-1)}, synchronize_session=False)
            db.commit()
            
            #Update the new assigned hospital db
            
            # new_user = {"name": user.first().name, "hosp_name": hosp.first().name}
            # new_user_data = models.AssignedHosp(**new_user.dict())
            # db.add(new_user_data)
            # db.commit()
            # db.refresh(new_user_data)

            print(f"Assigned {user.first().name} to {hosp.first().name}")
        else:
            print("Hospital is out of slots.")
            # del_hosp = db.query(models.Hospital).filter(models.Users.id == user_choice)
            # del_hosp.delete(synchronize_session=False)
        
        
        # user.delete(synchronize_session=False)
        # else:
        #     # Remove hosp from db if slots

            

    return user_list
