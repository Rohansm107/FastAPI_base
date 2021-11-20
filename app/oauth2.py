from jose import JWTError,jwt
from datetime import datetime,timedelta
from typing import Optional

from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")

# secret key
SECRET_KEY = settings.secret_key
# algorithm
ALGORITHM = settings.algorithm
# expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id:str=payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        token_data=schemas.Tokendata(id=user_id)
    except JWTError:
        credentials_exception
    
    return token_data


def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={
        "WWW-Authenticate":"Bearer"})

    token=verify_access_token(token,credential_exception)

    user=db.query(models.User).filter(models.User.id==token.id).first()

    return user
