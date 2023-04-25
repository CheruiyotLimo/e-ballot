from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
import requests
from Scripts import randomizer
from . import hosp, users, auth

router = APIRouter(
    prefix="/final",
    tags=["Final"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_to_final_list(entry: schemas.FinalCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Post request to update the final allocated list on successfull selection"""

    # Verify user is an admin
    oauth2.verify_admin(current_user)

    # Convert provided dictionary into a model dictionary.
    new_entry = models.AssignedHosp(**entry)

    # Update the assigned hosp db
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

