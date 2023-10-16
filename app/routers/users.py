from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, config
from Scripts import scripts, county_validator
from typing import Literal
import json

CHOICE = Literal["1", "2"]

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[schemas.UserReturn])
def get_all_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Get all the registered users. 
    Only admins can do this.
    """
    
    # Check if the current user is an admin. Currently taking admin as one whose reg_num matches the secret combination.
    oauth2.verify_admin(current_user)

    # Query database for all registered users
    users = db.query(models.Users).filter(models.Users.role==None, models.Users.posted==False).all()

    # # print(current_user.email)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users exist in the database!")
    # print(users)
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def register_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Sign up a user to the system."""
    # Verify it is a valid email address
    
    if not scripts.email_verifier(data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The email provided is not a valid email address")

    # Check if provided email and/or registration number exists in database
    user_email = db.query(models.Users).filter(models.Users.email == data.email)

    # Raise HTTP error if any exists.
    if user_email.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user already exists with similar email!!")
    
    # If an admin, hash the reg_num to abstract the admin secret in the database.
    if data.reg_num == config.settings.admin_reg:
        new_reg = utils.hash(data.reg_num)
        data.reg_num = new_reg
        data.role= "admin"

    # Hash password before storing in the database.
    new_password = utils.hash(data.password)
    data.password = new_password

    # Convert provided dictionary into a model dictionary.
    # data = models.Users(**data.dict())

    # Add user to the database.
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.patch("/{user_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def patch_user(user_data: schemas.UserUpdate, user_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """PATCH request to update user choice column"""
    ### Possibly deprecated


    # verify the user is an admin
    oauth2.verify_admin(current_user)

    # Query db for th current user
    user = db.query(models.Users).filter(models.Users.id == user_id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user exists")
    
    # Update the new choice column
    user.update(user_data, synchronize_session=False)

    # Commit changes
    db.commit()

    return user.first()

@router.patch("/choice/{choice}/", status_code=status.HTTP_201_CREATED)
def choose_hospital(user_data: schemas.UserUpdate, choice: CHOICE, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """PATCH request to update each user's choice.
       To be utilized by the client.
    """
    # QUery the db for the user
    user = db.query(models.Users).filter(models.Users.id == current_user.id)
 
    if not user.first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to log in to perform this action")

    if user.first().role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid action for type of user.")
    
    # Check for indicated user choice
    if choice == "1":
        user.update(user_data.dict(), synchronize_session=False)
        print("Successfully made your first choice.")
    else:
        # Check first choice has been made
        if not user.first().first_choice:
            print(2)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Can't make second choice before first. Please make first choice.")
        # Check second choice is a valid
        print(1)
        if not county_validator.county_validator(user.first().first_choice, user_data.first_choice, current_user, db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You cannot select two hospitals in the same county. Please choose another.")
        
        updated_data = {"second_choice": user_data.first_choice}
        # update the db
        user.update(updated_data, synchronize_session=False)
        print("Successfully made your second choice.")

    db.commit()    
    print(user.first())
    print(type(user.first()))
    return user.first()

@router.patch("/posted/", status_code=status.HTTP_201_CREATED)
def update_posted(posted_status: schemas.UserUpdatePosted, user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """PATCH request to update each user's posted status.
       To be utilized by the admin.
    """
    user = db.query(models.Users).filter(models.Users.id == user_id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User doess not exist")
    
    user.update(posted_status, synchronize_session=False)
    return "Succesfully updated posted status"
    

@router.post('/build/', status_code=status.HTTP_201_CREATED)
def build_users(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    # verify the user is an admin
    oauth2.verify_admin(current_user)

    user_list = {
        "Caleb": ["H31/2189/1017", "Caleb Musyoki", "calmus@students.uonbi.ac.ke", "calmus103"],
        "Limo": ["H31/2700/1027", "Yony Limo", "yony@students.uonbi.ac.ke", "oakeart"],
        "Abel": ['H31/2010/1987', 'Gakuya Mwangi', 'gaks@students.uonbi.ac.ke', 'mkm'],
        'Kipsang': ['H31/2182/1192', 'Elijah Kipsang', 'kips@students.uonbi.ac.ke', 'kips137'],
        'Ogutu': ['H31/1290/1298', 'Livingstone Ogutu', 'livi@students.uonbi.ac.ke', 'rockofages'],
        'Rynah': ['H31/24664/2017', 'Rynah Aluvisi', 'rynah@students.uonbi.ac.ke', 'mumbai'],
        'Too': ['H31/1267/1098', 'Holida Too', 'holi@students.uonbi.ac.ke', 'itsaholiday'],
        'Marie': ['H31/6235/2017', 'Marie Korie', 'marie@students.uonbi.ac.ke', 'mariempoa'],
        'Panthre': ['H31/2156/4879', 'Jagavan Panthre', 'panthre@students.uonbi.ac.ke', 'kalasingha'],
        'Rama': ['H31/2015/2364', 'Rama Njoki', 'rama@students.uonbi.ac.ke', 'rampapapam']
    }

    for _, v in user_list.items():
        user = {
            'reg_num': v[0],
            'name': v[1],
            'email': v[2],
            'password': v[3]
        }
        # user_json = json.dumps(user)
        user = models.Users(**user)
        register_user(data=user, db=db)
    
    return 'Successfully created all users!'