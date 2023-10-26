from fastapi import APIRouter, HTTPException, status, Depends
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from Scripts import randomizer
from . import hosp, users, auth, final
import json, time
from typing import Literal
from sqlalchemy.sql.expression import func
import random

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get('/', status_code=status.HTTP_201_CREATED)
def get_numbers(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    first_choice_students = 0
    second_choice_students = 0
    
    # Establish the user is an admin
    oauth2.verify_admin(current_user)
    
    # Retrieve posted students.
    all_users = db.query(models.AssignedHosp).all()
    
    all_students_number = len(all_users)
    
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users have been posted!")
    
    for student in all_users:
        user = db.query(models.Users).filter(models.Users.email==student.email)
        
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Student with email: {student.email} doesnt exist')
        
        user_first_choice = db.query(models.Hospital).filter(models.Hospital.id == user.first().first_choice).first()
        user_second_choice = db.query(models.Hospital).filter(models.Hospital.id == user.first().second_choice).first()
        
        if user_first_choice.name == student.hosp_name:
            first_choice_students += 1
            continue
        elif user_second_choice.name == student.hosp_name:
            second_choice_students += 1
        
    print(first_choice_students)
    print(second_choice_students)
    print(all_students_number)
    probability = round((((first_choice_students/all_students_number) + (second_choice_students/all_students_number)) * 100), 2)
    
    satisfaction = round((((first_choice_students/all_students_number) + ((second_choice_students/all_students_number)*0.8)) * 100), 2)
    
    return f"The probality of getting either of your choices is {probability} %, while the overall satisfaction rate is {satisfaction} %."



    