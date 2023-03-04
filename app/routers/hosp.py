from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from typing import Optional

router = APIRouter(
    prefix="/hosps",
    tags=["Hospitals"]
)

# GET request for a user to receive all available hospital
@router.get("/", status_code=status.HTTP_200_OK)
def get_all_hospitals(current_user: int = Depends(oauth2.get_current_user), db: Session = (Depends(get_db)), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    """
    GET request for a user to receive all available hospitals.
    with defined query parameters allowing for modification of returned results.
    """
    print(f"Currently logged in as: {current_user.name}")

    hosps = db.query(models.Hospital).filter(models.Hospital.name.contains(search)).limit(limit).offset(skip).all()

    if not hosps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are currently no open hospitals.")

    return hosps

@router.post("/choice", status_code=status.HTTP_201_CREATED)
def choose_hospital(hospital_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """POST request for a user to declare a hospital of their choice for placement."""
    
    print("123")
    # Query hosp database for the specified choice
    choice = db.query(models.Hospital).filter(models.Hospital.id == hospital_id).first()

    if not choice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no hospital with id {hospital_id}")
    print("tou")
    # Get current active user
    # user = db.query(models.Users).filter(models.Users.email == current_user.email).first()

    # Update their choices column
    current_user.choice = choice.id
    print("me")
    # Refresh the database
    db.commit()
    db.refresh(current_user)

    return f"Your chose {choice}"

  

