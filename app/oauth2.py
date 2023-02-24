from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

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

