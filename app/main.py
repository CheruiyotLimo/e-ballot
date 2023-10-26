from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .db import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils, oauth2
from .routers import auth, users, hosp, admin, final, analytics, builds
import requests
from typing import Optional

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(hosp.router)
app.include_router(admin.router)
app.include_router(final.router)
app.include_router(analytics.router)
app.include_router(builds.router)


@app.get("/")
async def root():
    return {"message": "The pathway to your internship future."}


# @app.get("/call-root")
# async def call_root(current_user: int = Depends(oauth2.get_current_user), db: Session = (Depends(get_db)), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
#     choice_1 = {"first_choice": 5}
#     choice_2 = {"first_choice": 2}

#     return users.patch_user(user_data=choice_1, user_id=26, current_user=current_user, db=db)

    return "Success!!!!!"