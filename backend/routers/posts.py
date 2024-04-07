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

class Post(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime
    owner: int
    comment_amount: int
    owner_name: str

class GetPostsResponse(BaseModel):
    posts: List[Post]
    pagination: models.Pagination

@router.post('/create', status_code=201, response_model=Post, summary="Create a new post")
def create_post(data: CreatePostPayload, db: db_dependency, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token_data = auth_utils.verify_token_access(creds.credentials)

    user = db.query(models.User).where(models.User.id == token_data.id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Encountered error when verifying user")
    else:
        new_post = models.Post(title=data.title, text=data.text, owner=user.id)
        db.add(new_post)
        db.commit()

        return {    
            'id': new_post.id,
            'title': new_post.title,
            'text': new_post.text,
            'created_at': new_post.created_at,
            'owner': new_post.owner,
            'comment_amount': new_post.comment_amount,
            'owner_name': user.username
        }
    
@router.delete("/delete", status_code=200, response_model=models.MessageResponse, summary="Delete an existing post")
def delete_post(id: int, db: db_dependency, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token_data = auth_utils.verify_token_access(creds.credentials)

    post = db.query(models.Post).where(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post is not found")
    elif str(post.owner) != token_data.id:
        raise HTTPException(status_code=401, detail="You have no access to modify this post")
    else:
        db.delete(post)
        db.commit()
        

    return { "message": "success" }

@router.get('/', status_code=200, response_model=GetPostsResponse, summary="Get posts for Feed page or posts of a specific user")
def get_posts(db: db_dependency, page: int = Query(1, ge=1), per_page: int = Query(5, ge=1, le=100), uid: int | None = None):
    if uid is None:
        query = db.query(models.Post)
    else:
        query = db.query(models.Post).filter(models.Post.owner == uid)

    total_posts = query.with_entities(func.count(models.Post.id)).scalar()
    total_pages = (total_posts + per_page - 1) // per_page
    offset = (page - 1) * per_page

    posts = query.order_by(desc(models.Post.created_at)).offset(offset).limit(per_page).all()

    names = {}

    def get_user_name(id):
        user = db.query(models.User).where(models.User.id == id).first()
        if user:
            names[id] = user.username
            return user.username
        else:
            return 'Unknown'

    named_posts = [{    
        'id': p.id,
        'title': p.title,
        'text': p.text,
        'created_at': p.created_at,
        'owner': p.owner,
        'comment_amount': p.comment_amount,
        'owner_name': names[p.owner] if p.owner in names else get_user_name(p.owner)
    } for p in posts]

    return { 
        "posts": named_posts,
        "pagination": {
            "is_last": page >= total_pages,
            "total_pages": total_pages,
            "total_entries": total_posts,
        }
    }

@router.get('/{id}', status_code=200, response_model=Post, summary="Get a single post")
def get_post(db: db_dependency, id: int):
    post = db.query(models.Post).where(models.Post.id == id).first()
    user = db.query(models.User).where(models.User.id == post.owner).first()
    return {    
        'id': post.id,
        'title': post.title,
        'text': post.text,
        'created_at': post.created_at,
        'owner': post.owner,
        'comment_amount': post.comment_amount,
        'owner_name': user.username
    }


