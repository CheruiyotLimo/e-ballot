from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union



class UserCreate(BaseModel):
    reg_num: str
    name: str
    email: EmailStr
    password: str
    first_choice: Optional[int] = None
    second_choice: Optional[int] = None
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

class Token(BaseModel):
    access_token: str
    token_type: str

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
    first_choice: Optional[Union[int, str]] = None
    second_choice: Optional[Union[int, str]] = None

class UserChoice(UserUpdate):
    name: str

class HospAssign(BaseModel):
    name: str
    hosp_name: str

class HospUpdate(BaseModel):
    slots: int

class FinalCreate(BaseModel):
    name: str
    hosp_name: str

# class UserUpdateTwo(BaseModel):
#     choice: