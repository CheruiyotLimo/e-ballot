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
    
    # Verify current user
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to log in.")

    # Query db for hospital
    hosp = db.query(models.Hospital).filter(models.Hospital.id == id)
    if not hosp.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital does not exist! Choose another")
    # print(hosp.first())
    return hosp.first()

@router.patch("/choice/{hosp_id}", status_code=status.HTTP_201_CREATED)
def choose_hospital(hosp: schemas.UserUpdate, hosp_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """POST request for a user to declare a hospital of their choice for placement."""
    ## Appears to have been remodeled and moved
  
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

  
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_hospital(hosp_data: schemas.HospCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ POST request for updating the hospital database"""

    # Check if user is authorized ## Will come to add admin requirement later
    oauth2.verify_admin(current_user)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to make this change.")
    
    # Check if the hospital exists
    hosp = db.query(models.Hospital).filter(models.Hospital.name == hosp_data.name).first()
    if hosp:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hospital already exists.")
    
    # Convert the dictionary to a model dictionary
    hosp_data = models.Hospital(**hosp_data.dict())

    # Add new hospital to the database
    db.add(hosp_data)
    db.commit()
    db.refresh(hosp_data)
    print(type(hosp_data))
    print(hosp_data)
    return hosp_data

@router.patch("/{hosp_id}", status_code=status.HTTP_201_CREATED)
def patch_hospital_slots(hosp: schemas.HospUpdate, hosp_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Patch request to update the number of slots available in a hospital"""
    ### ***** This is the one in use
    # Verify user is an admin
    oauth2.verify_admin(current_user)

    # Query db for hospital
    hospital = db.query(models.Hospital).filter(models.Hospital.id == hosp_id)
    
    if not hospital.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hospital with id: {hosp_id} doesnt exist")
    
    # Update the hospital slots
    hospital.update(hosp, synchronize_session=False)  ## Interesting bug here. When I use hosp.dict(), it runs fine on Postman dn tests but fails on use from the admin magic_maker file and vice versa
    db.commit()

    return hospital.first()

@router.delete("/{hosp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hospital(hosp_id: int, current_user = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Delete request to remov a hospital from the db"""

    # Verify user is an admin
    oauth2.verify_admin(current_user)

    # Query hospital db
    hospital = db.query(models.Hospital).filter(models.Hospital.id == hosp_id)

    if not hospital.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hospital with id: {hosp_id} doesnt exist")

    # Update the db
    hospital.delete(synchronize_session=False)
    db.commit()
    return {"Message": "Successfully deleted hospital"}

@router.post('/build/', status_code=status.HTTP_201_CREATED)
def build_hosps(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    # verify the user is an admin
    oauth2.verify_admin(current_user)

    hosp_list = {
        "KNH": ["Kenyatta National Hospital", "Nairobi", "47", 3],
        "MTRH": ['Moi Teaching & Referral Hospital', 'Uasin Gishu', '27', 2],
        'NPGH': ['Nakuru Provincial General Hospital', 'Nakuru', '32', 1],
        'CGRH': ['Coast General Referral Hospital', 'Mombasa', '1', 2],
        'KRH': ['Thika Level V', 'Kiambu', '22', 2],
        'Mbagathi': ['Mbagathi Hospital', 'Nairobi', '47', 1]
    }

    for _, v in hosp_list.items():
        hosp = {
            'name': v[0],
            'county_name': v[1],
            'county_num': v[2],
            'slots': v[3]
        }

        hosp = models.Hospital(**hosp)

        add_hospital(hosp_data=hosp, db=db, current_user=current_user)
    return 'Successfully built all hospitals!'