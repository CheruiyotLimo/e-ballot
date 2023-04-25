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
import json, time
from typing import Literal
from sqlalchemy.sql.expression import func

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

Rounds = Literal[1, 2]





def first_round(select_round: Rounds, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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


        # Check user choice based on round of selection
        if select_round == 1:
            user_choice = user.first().first_choice
        elif select_round == 2:
            user_choice = user.first().second_choice
        print(user_choice)

        # Query the hospital db for the hospital
        hospital = hosp.get_one_hospital(id=user_choice, current_user=current_user, db=db)
        
        # If hospital has no slots, nullify user's choice
            
    
        if hospital.slots >= 1:
            # Update hospital slots
            new_slots = {"slots": hospital.slots-1}
            json_obj = json.dumps(new_slots)
            new_slots = json.loads(json_obj)
            hosp.patch_hospital_slots(hosp=new_slots, hosp_id=user_choice, current_user=current_user, db=db)
            
            # Patch user_choice column
            if select_round == 1:
                deprecated_choice = {"first_choice": None, "second_choice": None}
            elif select_round == 2:
                deprecated_choice = {"first_choice": None, "second_choice": None}
            users.patch_user(user_data=deprecated_choice, user_id=user.first().id, current_user=current_user, db=db)

            # Update the new assigned hospital db
            allocated_user = {"name": user.first().name, "hosp_name": hospital.name}
            final.add_to_final_list(entry=allocated_user, current_user=current_user, db=db)

            print(f"Allocated {allocated_user['name']} to {allocated_user['hosp_name']} in round {select_round}")
        else:
            print(f"{hospital.name} is out of slots.")
            # Remove hosp from the db
            # hosp.delete_hospital(hosp_id=user_choice, current_user=current_user, db=db)
        time.sleep(1)   
        
        
        # user.delete(synchronize_session=False)
        # else:
        #     # Remove hosp from db if slots
    
    
    return user_list



def final_pass(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """GET request to execute final pass which will match random users to a random hospital"""

    # verify admin
    oauth2.verify_admin(current_user)

    # Needs a loop to account for all unselected applicants
    all_users = db.query(models.Users).filter(models.Users.role == None, models.Users.first_choice != None, models.Users.second_choice!=None).all()
    while all_users:
        # select a random user
        user = db.query(models.Users).order_by(func.random())

        # select a random hospital
        hospital = db.query(models.Hospital).order_by(func.random())

        if hospital.first().slots >= 1:
            # Update hospital slots
            new_slots = {"slots": hospital.first().slots-1}
            json_obj = json.dumps(new_slots)
            new_slots = json.loads(json_obj)
            hosp.patch_hospital_slots(hosp=new_slots, hosp_id=hospital.first().id, current_user=current_user, db=db)
            
            # Update the new assigned hospital db
            allocated_user = {"name": user.first().name, "hosp_name": hospital.first().name}
            final.add_to_final_list(entry=allocated_user, current_user=current_user, db=db)

            # Delete the user from the all_users list
            all_users.remove(user.first())        
        else:
            print(f"{hospital.first().name} is out of slots.")


@router.get("/", status_code=status.HTTP_201_CREATED)
def magic_maker(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    first_round(select_round=1, current_user=current_user, db=db)
    first_round(select_round=2, current_user=current_user, db=db)
    final_pass(current_user=current_user, db=db)
    return "Successfully allocated hospitals."
    