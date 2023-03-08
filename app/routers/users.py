from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, config
# from ...Scripts import scripts


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[schemas.UserReturn])
def get_users( db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Get all the registered users. 
    Only admins can do this.
    """
    
    # Check if the current user is an admin. Currently taking admin as one whose reg_num matches the secret combination.
    oauth2.verify_admin(current_user)

    # Query database for all registered users
    users = db.query(models.Users).filter(models.Users.role == None).all()

    # print(current_user.email)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {id} doesn,t exist")
    # print(users)
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def register_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Sign up a user to the system."""
    # Verify it is a valid email address
    # if not scripts.email_verifier(data.email):
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The email provided is not a valid email address")

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
    data = models.Users(**data.dict())

    # Add user to the database.
    db.add(data)
    db.commit()
    db.refresh(data)
    return data