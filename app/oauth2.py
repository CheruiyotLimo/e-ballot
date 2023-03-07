from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from . import schemas, db, models
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(user_data: dict):
    """Creates an access token for the user when they log in"""
    
    # Create a copy of the original data
    to_encode = user_data.copy()

    # Update expiry time
    expiry_duration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expiry": jsonable_encoder(expiry_duration)})

    # Encode the user_data using JWT
    encoded_data = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    # Return the generated token to user
    return encoded_data 


def verify_access_token(token: str, cred_exception):
    """Verify the validity of the access token."""

    try:
        # Decode the passed in token
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        # Extract user_id
        user_id = payload.get("user_id")
        
        #Extract reg_num
        user_reg_num = payload.get("reg_num")

        # Check for valid arguments
        if not user_id and user_reg_num:
            raise cred_exception
        
        # Run data through pydantic schema
        token_data = schemas.TokenData(id=user_id, reg_num=user_reg_num)
        
    except JWTError:
        raise cred_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)):
    """Checks and returns the current logged in user"""

    # *TO REFACTOR* Defining cred_exception
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})

    # Verify the token
    token_data = verify_access_token(token, cred_exception)

    #Query the db for the user
    user = db.query(models.Users).filter(models.Users.id == token_data.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You need to log in first")
    
    # Return the user
    print(f"Current active user: {user.name}")
    return user