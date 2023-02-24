from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class UserCreate(BaseModel):
    reg_num: str
    name: str
    email: EmailStr
    password: str

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