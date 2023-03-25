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
def get_all_hospitals(current_user: int = Depends(oauth2.get_current_user), db: Session = (Depends(get_db)), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """
    GET request for a user to receive all available hospitals.
    with defined query parameters allowing for modification of returned results.
    """
    # print(f"Currently logged in as: {current_user.name}")

    hosps = db.query(models.Hospital).filter(models.Hospital.name.contains(search)).limit(limit).offset(skip).all()

    if not hosps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are currently no open hospitals.")

    return hosps

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_one_hospital(id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = (Depends(get_db))):
    """Get a single hospital by id."""
    
    #Verify current user
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to log in.")

    # Query db for hospital
    hosp = db.query(models.Hospital).filter(models.Hospital.id == id)
    print(hosp.first())
    return hosp

@router.patch("/choice/{hosp_id}", status_code=status.HTTP_201_CREATED)
def choose_hospital(hosp: schemas.UserUpdate, hosp_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """POST request for a user to declare a hospital of their choice for placement."""

  
    # Query hosp database for the specified choice
    choice = db.query(models.Hospital).filter(models.Hospital.id == hosp_id)

    if not choice.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no hospital with id {hosp_id}")

    # Get current active user
    user = db.query(models.Users).filter(models.Users.email == current_user.email)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not logged in.")
    
    # Update the choice for current active user
    user.update(hosp.dict(), synchronize_session=False)

    # db.add(updated_user)
    db.commit()
    # db.refresh(user)

    return f"You chose {choice.first().name}"

  
@router.post("/", response_model=schemas.HospReturn, status_code=status.HTTP_201_CREATED)
def add_hospital(hosp_data: schemas.HospCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ POST request for updating the hospital database"""

    # Check if user is authorized ## Will come to add admin requirement later
    oauth2.verify_admin(current_user)

    # user = db.query(models.Users).filter(models.Users.email == current_user.email).first()

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to make this change.")
    
    # Check if the hospital exists
    hosp = db.query(models.Hospital).filter(models.Hospital.name == hosp_data.name).first()
    if hosp:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hospital already exists.")
    
    # Convert the dictionary to a model dictionary
    new_hosp = models.Hospital(**hosp_data.dict())

    # Add new hospital to the database
    db.add(new_hosp)
    db.commit()
    db.refresh(new_hosp)

    return hosp_data

@router.put("/{hosp_id}", status_code=status.HTTP_201_CREATED)
def patch_hospital_slots(hosp: schemas.HospUpdate, hosp_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Patch request to update the number of slots available in a hospital"""

    # Verify user is an admin
    oauth2.verify_admin(current_user)

    # Query db for hospital
    hospital = db.query(models.Hospital).filter(models.Hospital.id == hosp_id)
    
    if not hospital.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hospital with id: {hosp_id} doesnt exist")
    
    # Update the hospital slots
    hospital.update(hosp.dict(), synchronize_session=False)
    db.commit()

    return hospital.first()