from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dependencies import db_dependency
import auth_utils
import models

router = APIRouter(
    prefix="/auth"
)

token_auth_scheme = HTTPBearer()

class UserCreds(BaseModel):
    name: str
    pw: str

@router.post("/signup", status_code=201, response_model=UserCreds)
def sign_up(creds: UserCreds, db: db_dependency):
    user = db.query(models.User).where(models.User.username == creds.name).first()

    if user:
        raise HTTPException(status_code=403, detail="User with this name already exists")

    hashed_pw = auth_utils.hash_password(creds.pw)
    new_user = models.User(username=creds.name, hashed_pw=hashed_pw)
    db.add(new_user)
    db.commit()

    return { "name": new_user.username, "pw": creds.pw }

@router.post("/signin", response_model=auth_utils.Token)
def sign_in(creds: UserCreds, db: db_dependency):
    user = db.query(models.User).filter(models.User.username == creds.name).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    elif not auth_utils.verify_password(creds.pw, user.hashed_pw):
        raise HTTPException(status_code=401, detail="The password is incorrect")
    else:
        access_token = auth_utils.create_access_token(data={"user_id": user.id})
        return { "access_token": access_token, "token_type": "bearer" }
    
@router.get("/current")
def get_current(db: db_dependency, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    data = auth_utils.verify_token_access(
        creds.credentials, 
        HTTPException(
            status_code=401,
            detail="Could not Validate Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    )
    
    user = db.query(models.User).filter(models.User.id == data.id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Your token is valid, but user of passed id is not found")
    else:
        return user
    
