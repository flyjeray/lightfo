from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import db_dependency
import models
import auth_utils

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

token_auth_scheme = HTTPBearer()

class CreatePostPayload(BaseModel):
    title: str
    text: str

class CreatePostResponse(BaseModel):
    id: int

@router.post('/create', status_code=201, response_model=CreatePostResponse, summary="Create a new post")
def create_post(data: CreatePostPayload, db: db_dependency, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token_data = auth_utils.verify_token_access(creds.credentials)

    user = db.query(models.User).where(models.User.id == token_data.id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Encountered error when verifying user")
    else:
        new_post = models.Post(title=data.title, text=data.text)
        db.add(new_post)
        db.commit()
        db.flush()
        new_relation = models.UserPostRelation(post_id=new_post.id, user_id=user.id)
        db.add(new_relation)
        db.commit()
        new_post.relation = new_post.id
        db.commit()

        return { "id": new_post.id }

