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

@router.put("/choice", status_code=status.HTTP_201_CREATED)
def choose_hospital(hosp_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """POST request for a user to declare a hospital of their choice for placement."""

    print("123")
    # Query hosp database for the specified choice
    choice = db.query(models.Hospital).filter(models.Hospital.id == hosp_id).first()

    if not choice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no hospital with id {hosp_id}")
    print("tou")
    # Get current active user
    user = db.query(models.Users).filter(models.Users.email == current_user.email)

    # Update their choices column
    user.update({"choices": choice.id}, synchronize_session=False)  
    print("me")
    # Refresh the database
    db.commit()
    db.refresh(user)

    return f"Your chose {choice}"

  
@router.post("/", response_model=schemas.HospReturn, status_code=status.HTTP_201_CREATED)
def add_hospital(hosp: schemas.HospCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ POST request for updating the hospital database"""

    # Check if user is authorized ## Will come to add admin requirement later
    user = db.query(models.Users).filter(models.Users.email == current_user.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to make this change.")
    
    #C
    
    # Convert the dictionary to a model dictionary
    new_hosp = models.Hospital(**hosp.dict())

    # Add new hospital to the database
    db.add(new_hosp)
    db.commit()
    db.refresh(new_hosp)

    return hosp
