# Query for all users.
# Pick them randomnly, checking their first choice and assigning it to them and removing from db.
# If not, remove their choice and leave them in the db for a second run.

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
import requests
from Scripts import randomizer, serializer, qrcode
from . import hosp, users, auth, final
import json, time
from typing import Literal
from sqlalchemy.sql.expression import func
import random

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

Rounds = Literal[1, 2]

second_round_list = []
final_round_list = []




def first_round(select_round: Rounds, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Get request to execute first phase of balloting. Get all the users, randomize their selection and assign them the centers."""

    # Ensure the user is an admin
    oauth2.verify_admin(current_user)

    # Get all registered users in a list
    user_list = users.get_all_users(db=db, current_user=current_user)

    # print(current_user.email)
    if not user_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No registered users exist")

    # Access user ids from randomizer scripts
    # Need a statement to loop through the options.
    
    # New sorting logic
    while user_list:
        curr_user = random.choice(user_list)
        
         # Check user choice based on round of selection
        if select_round == 1:
            user_choice = curr_user.first_choice
        elif select_round == 2:
            user_choice = curr_user.second_choice
        print(f"{curr_user.name}'s choice is: {user_choice}")
        
        # Query the hospital db for the hospital
        hospital = hosp.get_one_hospital(id=user_choice, current_user=current_user, db=db)
        
        if hospital and hospital.slots >= 1:
            
            # Update hospital slots
            new_slots = {"slots": hospital.slots-1}
            json_obj = json.dumps(new_slots)
            new_slots = json.loads(json_obj)
            hosp.patch_hospital_slots(hosp=new_slots, hosp_id=user_choice, current_user=current_user, db=db)
            
            # Generate serial number
            serial_number = serializer.generate_alphanumeric_sequence()
            
            # Generate a qrcode
            qrcode_binary = qrcode.qrcode_generator(curr_user.name, hospital.name, serial_number)

            # Update the new assigned hospital db
            allocated_user = {"name": curr_user.name, "hosp_name": hospital.name, "email": curr_user.email, "serial_number": serial_number, 'qrcode': qrcode_binary}
            final.add_to_final_list(entry=allocated_user, current_user=current_user, db=db)
            
            # Update analysis table
            allot_user = {'name': curr_user.name, 'email': curr_user.email, 'first_choice': curr_user.first_choice, 'second_choice': curr_user.second_choice, 'alloc_hosp': hospital.id}
            final.gen_analysis(entry=allot_user, current_user=current_user, db=db)
            
            # Update user posted status
            posted_status = {'posted': True}
            users.update_posted(posted_status, user_id=curr_user.id, db=db, current_user=current_user)

            user_list.remove(curr_user)

            print(f"Allocated {allocated_user['name']} to {allocated_user['hosp_name']} in round {select_round}")
            
        else:
            print(f"{hospital.name} is out of slots.")
            user_list.remove(curr_user)
            
            # Remove hosp from the db
            # hosp.delete_hospital(hosp_id=user_choice, current_user=current_user, db=db)
        # time.sleep(1)   
    

            
        
    
    # # while user_list:
    # for id in randomizer.new_rand(user_list):

    #     user = db.query(models.Users).filter(models.Users.id == id)

    #     print(id) 
    #     if not user.first():
    #         continue

    #     if not user.first().first_choice:
    #         continue

    #     # Check user choice based on round of selection
    #     if select_round == 1:
    #         user_choice = user.first().first_choice
    #     elif select_round == 2:
    #         user_choice = user.first().second_choice
    #     print(user_choice)

    #     # Query the hospital db for the hospital
    #     hospital = hosp.get_one_hospital(id=user_choice, current_user=current_user, db=db)
        
    #     # If hospital has no slots, nullify user's choice
            
    
    #     if hospital and hospital.slots >= 1:
    #         # Update hospital slots
    #         new_slots = {"slots": hospital.slots-1}
    #         json_obj = json.dumps(new_slots)
    #         new_slots = json.loads(json_obj)
    #         hosp.patch_hospital_slots(hosp=new_slots, hosp_id=user_choice, current_user=current_user, db=db)
            
    #         # Patch user_choice column
    #         if select_round == 1:
    #             deprecated_choice = {"first_choice": None, "second_choice": None}
    #         elif select_round == 2:
    #             deprecated_choice = {"first_choice": None, "second_choice": None}
    #         users.patch_user(user_data=deprecated_choice, user_id=user.first().id, current_user=current_user, db=db)

    #         # Update the new assigned hospital db
    #         allocated_user = {"name": user.first().name, "hosp_name": hospital.name}
    #         final.add_to_final_list(entry=allocated_user, current_user=current_user, db=db)

    #         print(f"Allocated {allocated_user['name']} to {allocated_user['hosp_name']} in round {select_round}")
    #     else:
    #         print(f"{hospital.name} is out of slots.")
    #         # Remove hosp from the db
    #         # hosp.delete_hospital(hosp_id=user_choice, current_user=current_user, db=db)
    #     time.sleep(1)   
    
    
    # user.delete(synchronize_session=False)
    # else:
    #     # Remove hosp from db if slots

    
    # return user_list



def final_pass(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """GET request to execute final pass which will match random users to a random hospital"""

    # verify admin
    oauth2.verify_admin(current_user)

    # Needs a loop to account for all unselected applicants
    all_users = users.get_all_users(db=db, current_user=current_user)
    print(len(all_users))
    
    while all_users:
        curr_user = random.choice(all_users)

        # select a random hospital
        # all_hosps = hosp.get_all_hospitals(current_user=current_user, db=db)
        all_hosps = db.query(models.Hospital).filter(models.Hospital.slots >= 1).all()
        hospital = random.choice(all_hosps)

        if hospital.slots >= 1:
            # Update hospital slots
            new_slots = {"slots": hospital.slots-1}
            json_obj = json.dumps(new_slots)
            new_slots = json.loads(json_obj)
            hosp.patch_hospital_slots(hosp=new_slots, hosp_id=hospital.id, current_user=current_user, db=db)
            
            # Generate serial number
            serial_number = serializer.generate_alphanumeric_sequence()
            
            # Generate a qrcode
            qrcode_binary = qrcode.qrcode_generator(curr_user.name, hospital.name, serial_number)

            
            # Update the new assigned hospital db
            allocated_user = {"name": curr_user.name, "hosp_name": hospital.name, "email": curr_user.email, "serial_number": serial_number, 'qrcode': qrcode_binary}
            final.add_to_final_list(entry=allocated_user, current_user=current_user, db=db)
            
            # Update analysis table
            allot_user = {'name': curr_user.name, 'email': curr_user.email, 'first_choice': curr_user.first_choice, 'second_choice': curr_user.second_choice, 'alloc_hosp': hospital.id}
            final.gen_analysis(entry=allot_user, current_user=current_user, db=db)
            
            # Update user posted status
            posted_status = {'posted': True}
            users.update_posted(posted_status, user_id=curr_user.id, db=db, current_user=current_user)

            # Delete the user from the all_users list
            all_users.remove(curr_user)       
        else:
            print(f"{hospital.name} is out of slots.")
            all_hosps.remove(hospital)
        # time.sleep(1)


@router.get("/", status_code=status.HTTP_201_CREATED)
def magic_maker(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    # First phase
    first_round(select_round=1, current_user=current_user, db=db)
    print("\nDone with round 1.")
    time.sleep(2)

    # Second phase
    first_round(select_round=2, current_user=current_user, db=db)
    print("\nDone with round 2.")
    time.sleep(2)

    # Final phase
    final_pass(current_user=current_user, db=db)
    return "Successfully allocated hospitals."
    