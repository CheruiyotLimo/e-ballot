from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class UserCreate(BaseModel):
    reg_num: str
    name: str
    email: EmailStr
    password: str
    choice: Optional[int] = None
    role: Optional[str] = None

class UserReturn(BaseModel):
    id: str
    reg_num: str
    email: str

    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None
    reg_num: Optional[str] = None

class HospCreate(BaseModel):
    name: str
    county_name: str
    county_num: int
    slots: int

class HospReturn(BaseModel):
    name: str
    county_name: str
    slots: int

class UserUpdate(BaseModel):
    choice: int