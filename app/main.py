from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .db import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils, oauth2
from .routers import auth, users, hosp, admin, final
import requests
from typing import Optional
app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(hosp.router)
app.include_router(admin.router)
app.include_router(final.router)


@app.get("/")
async def root():
    return {"message": "The pathway to your internship future."}


@app.get("/call-root")
async def call_root(current_user: int = Depends(oauth2.get_current_user), db: Session = (Depends(get_db)), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return hosp.get_all_hospitals(current_user, db)
    return "Success"
