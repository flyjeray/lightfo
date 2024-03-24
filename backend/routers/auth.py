from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import db_dependency
import auth_utils
import models

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

token_auth_scheme = HTTPBearer()

class UserCreds(BaseModel):
    name: str
    password: str

class CurrentUserData(BaseModel):
    id: int
    username: str
    access_token: str

class SignResponse(BaseModel):
    access_token: str
    token_type: str
    name: str

@router.post("/signup", status_code=201, response_model=SignResponse, summary="Create a new user with a unique username")
def sign_up(creds: UserCreds, db: db_dependency):
    user = db.query(models.User).where(models.User.username == creds.name).first()

    if user:
        raise HTTPException(status_code=403, detail="User with this name already exists")

    hashed_pw = auth_utils.hash_password(creds.password)
    new_user = models.User(username=creds.name, hashed_pw=hashed_pw)
    db.add(new_user)
    db.commit()
    db.flush()
    access_token = auth_utils.create_access_token(data={"user_id": new_user.id})

    return { "access_token": access_token, "token_type": "bearer", "name": new_user.username }

@router.post("/signin", response_model=SignResponse, summary="Sign In with existing credentials")
def sign_in(creds: UserCreds, db: db_dependency):
    user = db.query(models.User).filter(models.User.username == creds.name).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    elif not auth_utils.verify_password(creds.password, user.hashed_pw):
        raise HTTPException(status_code=401, detail="The password is incorrect")
    else:
        access_token = auth_utils.create_access_token(data={"user_id": user.id})
        return { "access_token": access_token, "token_type": "bearer", "name": user.username }
    
@router.get("/current", response_model=CurrentUserData, summary="Get id and username of current logged user. This method is used for autologin")
def get_current_user(db: db_dependency, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    data = auth_utils.verify_token_access(creds.credentials)
    
    user = db.query(models.User).filter(models.User.id == data.id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Your token is valid, but user of passed id is not found")
    else:
        return { "id": user.id, "username": user.username, "access_token": creds.credentials }
    
