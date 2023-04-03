from app.routers import hosp
from app import oauth2, db
from fastapi import Depends
from sqlalchemy.orm import Session

def county_validator(choice1, choice2, current_user = Depends(oauth2.get_current_user), db: Session = Depends(db.get_db)):

    hosp1 = hosp.get_one_hospital(choice1, current_user=current_user, db=db)

    hosp2 = hosp.get_one_hospital(choice2, current_user=current_user, db=db)

    if hosp1.county_num == hosp2.county_num:
        return False
    return True