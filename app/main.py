from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .db import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .routers import auth, users, hosp, admin
import requests

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(hosp.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "The pathway to your internship future."}


# @app.get("/call-root")
# async def call_root():
#     # response = await root()

#     url = "http://127.0.0.1:8000/hosps"
#     results = requests.get(url)
#     print(results)
#     return {"response": results}

