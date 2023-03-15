from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .db import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .routers import auth, users, hosp, admin


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(hosp.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "The pathway to your internship future."}

