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
@router.get("/", response_model=schemas.HospReturn, status_code=status.HTTP_200_OK)
def get_all_hospitals(current_user: int = Depends(oauth2.get_current_user), db = Session(Depends(get_db)), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    """
    GET request for a user to receive all available hospitals.
    with defined query parameters allowing for modification of returned results.
    """
    print(f"Active user: {current_user}")

    hosps = db.query(models.Hospital).filter(models.Hospital.name.contains(search)).limit(limit).offset(skip).all()

    if not hosps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are currently no open hospitals.")

    return hosps
