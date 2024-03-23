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

class MessageResponse(BaseModel):
    message: str

@router.post('/create', status_code=201, response_model=CreatePostResponse, summary="Create a new post")
def create_post(data: CreatePostPayload, db: db_dependency, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token_data = auth_utils.verify_token_access(creds.credentials)

    user = db.query(models.User).where(models.User.id == token_data.id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Encountered error when verifying user")
    else:
        new_post = models.Post(title=data.title, text=data.text, owner=user.id)
        db.add(new_post)
        db.commit()
        db.flush()
        if user.posts is not None:
            user.posts = [*user.posts, new_post.id]
        else:
            user.posts = [new_post.id]
        db.commit()

        return { "id": new_post.id }
    
@router.delete("/delete", status_code=200, response_model=MessageResponse, summary="Delete an existing post")
def delete_post(id: int, db: db_dependency, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token_data = auth_utils.verify_token_access(creds.credentials)

    post = db.query(models.Post).where(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post is not found")
    elif str(post.owner) != token_data.id:
        raise HTTPException(status_code=401, detail="You have no access to modify this post")
    else:
        owner = db.query(models.User).where(models.User.id == post.owner).first()
        if owner and owner.posts is not None and post.id in owner.posts:
            owner.posts = [p_id for p_id in owner.posts if p_id != post.id]
        db.delete(post)
        db.commit()
        

    return { "message": "success" }

