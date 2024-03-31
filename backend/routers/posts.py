from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from database import db_dependency
from sqlalchemy import func, desc
from datetime import datetime
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

class Post(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime

class PostWithIDdOwner(Post):
    owner: int

class PostWithNamedOwner(Post):
    owner: str

class GetPostsResponse(BaseModel):
    posts: List[PostWithNamedOwner]
    pagination: models.Pagination

@router.post('/create', status_code=201, response_model=PostWithIDdOwner, summary="Create a new post")
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

        return new_post
    
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

@router.get('/', status_code=200, response_model=GetPostsResponse, summary="Get posts for main page")
def get_posts(db: db_dependency, page: int = Query(1, ge=1), per_page: int = Query(5, ge=1, le=100)):
    total_posts = db.query(func.count(models.Post.id)).scalar()
    total_pages = (total_posts + per_page - 1) // per_page
    offset = (page - 1) * per_page
    posts = db.query(models.Post).order_by(desc(models.Post.created_at)).offset(offset).limit(per_page).all()

    names = {}

    def get_user_name(id):
        user = db.query(models.User).where(models.User.id == id).first()
        if user:
            names[id] = user.username
            return user.username
        else:
            return 'Unknown'

    with_owner = [{    
        'id': p.id,
        'title': p.title,
        'text': p.text,
        'created_at': p.created_at,
        'owner': names[p.owner] if p.owner in names else get_user_name(p.owner)
    } for p in posts]

    return { 
        "posts": with_owner,
        "pagination": {
            "is_last": page == total_pages,
            "total_pages": total_pages,
            "total_entries": total_posts,
        }
    }

@router.get('/{id}', status_code=200, response_model=PostWithNamedOwner, summary="Get a single post")
def get_post(db: db_dependency, id: int):
    post = db.query(models.Post).where(models.Post.id == id).first()
    return post


