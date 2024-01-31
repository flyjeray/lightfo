import os
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, datetime
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/signin')

SECRET_KEY = os.getenv('AUTH_ENCRYPTION_KEY')
ALGORITHM = os.getenv('AUTH_ENCRYPTION_METHOD')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id: str

def hash_password(pw: str):
    return pwd_context.hash(pw)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token_access(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not Validate Credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        token_data = DataToken(id=str(id))
    except JWTError as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail="Could not Validate Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token_data

def verify_password(pw: str, hashed_pw: str):
    return pwd_context.verify(pw, hashed_pw)