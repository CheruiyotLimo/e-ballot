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
from . import hosp, users, auth, final
import json

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
        hospital = hosp.get_one_hospital(id=user_choice, current_user=current_user, db=db)
        
        if not hospital:
            deprecated_choice = {"choice": None}
            users.patch_user(user_data=deprecated_choice, user_id=user.first().id, current_user=current_user, db=db)
        
        else:
            if hospital.slots >= 1:

                # Update hospital slots
                new_slots = {"slots": hospital.slots-1}
                json_obj = json.dumps(new_slots)
                new_slots = json.loads(json_obj)
                hosp.patch_hospital_slots(hosp=new_slots, hosp_id=user_choice, current_user=current_user, db=db)
                
                # Update the new assigned hospital db
                allocated_user = {"name": user.first().name, "hosp_name": hospital.name}
                final.add_to_final_list(entry=allocated_user, current_user=current_user, db=db)

                print(f"Allocated {allocated_user['name']} to {allocated_user['hosp_name']}")
            else:
                print(f"{hospital.name} is out of slots.")
                # Remove hosp from the db
                # hosp.delete_hospital(hosp_id=user_choice, current_user=current_user, db=db)
           
        
        
        # user.delete(synchronize_session=False)
        # else:
        #     # Remove hosp from db if slots

            

    return user_list
