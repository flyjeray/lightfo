from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import db_dependency
from pydantic import BaseModel
from sqlalchemy import func, desc
from typing import List
from .users import User
from datetime import datetime
import models
import auth_utils

router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)

token_auth_scheme = HTTPBearer()

class Comment(BaseModel):
    id: int
    text: str
    post: int
    post_title: str
    created_at: datetime
    user: User

class PostCommentPayload(BaseModel):
    text: str

class GetCommentsResponse(BaseModel):
    comments: List[Comment]
    pagination: models.Pagination

@router.post('/add/{post_id}', status_code=201, response_model=Comment, description="Post a comment to a post")
def post_comment(db: db_dependency, post_id: int, payload: PostCommentPayload, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token_data = auth_utils.verify_token_access(creds.credentials)
    
    post = db.query(models.Post).where(models.Post.id == post_id).first()
    user = db.query(models.User).where(models.User.id == token_data.id).first()

    if post and user:
        comment = models.Comment(text=payload.text, post=post_id, user=user.id)
        db.add(comment)
        post.comment_amount = post.comment_amount + 1
        user.comment_amount = user.comment_amount + 1
        db.commit()
        db.flush()
        return {
            'id': comment.id,
            'text': comment.text,
            'created_at': comment.created_at,
            'post': post_id,
            'post_title': post.title,
            'user': {
                'id': user.id,
                'username': user.username
            }
        }
    else:
        raise HTTPException(status_code=500, detail="Error while validating User and Post")
    
@router.delete('/delete/{comment_id}', status_code=200, response_model=models.MessageResponse, description="Delete a comment")
def delete_comment(db: db_dependency, comment_id: int, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token_data = auth_utils.verify_token_access(creds.credentials)

    comment = db.query(models.Comment).where(models.Comment.id == comment_id).first()

    if comment is None:
        raise HTTPException(status_code=404, detail="Post is not found")
    elif str(comment.user) != token_data.id:
        raise HTTPException(status_code=401, detail="You have no access to modify this post")
    else:
        post = db.query(models.Post).where(models.Post.id == comment.post).first()
        user = db.query(models.User).where(models.User.id == comment.user).first()
        if post:
            post.comment_amount = post.comment_amount - 1
        if user:
            user.comment_amount = user.comment_amount - 1
        db.delete(comment)
        db.commit()

    return { 'message': 'success' }

@router.get('/{post_id}', status_code=200, response_model=GetCommentsResponse, description="Get comments for specific post")
def get_comments_for_post(db: db_dependency, post_id: int, page: int = Query(1, ge=1), per_page: int = Query(5, ge=1, le=100)):
    post = db.query(models.Post).where(models.Post.id == post_id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post is not found")

    query = db.query(models.Comment).where(models.Comment.post == post_id)

    total_comments = query.with_entities(func.count(models.Comment.id)).scalar()
    total_pages = (total_comments + per_page - 1) // per_page
    offset = (page - 1) * per_page

    comments = query.order_by(desc(models.Comment.created_at)).offset(offset).limit(per_page).all()

    users = {}

    def get_user(user_id):
        user = db.query(models.User).where(models.User.id == user_id).first()
        users[user_id] = user 
        return user  

    filled = [{    
        'id': c.id,
        'text': c.text,
        'post': c.post,
        'post_title': post.title,
        'created_at': c.created_at,
        'user': users[c.user] if c.user in users else get_user(c.user),
    } for c in comments]

    return {
        'comments': filled,
        "pagination": {
            "is_last": page >= total_pages,
            "total_pages": total_pages,
            "total_entries": total_comments,
        }
    }

@router.get('/user/{user_id}', status_code=200, response_model=GetCommentsResponse, description="Get comments for specific user")
def get_comments_for_user(db: db_dependency, user_id: int, page: int = Query(1, ge=1), per_page: int = Query(5, ge=1, le=100)):
    user = db.query(models.User).where(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User is not found")

    query = db.query(models.Comment).where(models.Comment.user == user_id)

    total_comments = query.with_entities(func.count(models.Comment.id)).scalar()
    total_pages = (total_comments + per_page - 1) // per_page
    offset = (page - 1) * per_page

    comments = query.order_by(desc(models.Comment.created_at)).offset(offset).limit(per_page).all()

    posts = {}

    def get_post(post_id):
        post = db.query(models.Post).where(models.Post.id == post_id).first()
        posts[post_id] = post.title
        return post.title  

    filled = [{    
        'id': c.id,
        'text': c.text,
        'post': c.post,
        'post_title': posts[c.post] if c.post in posts else get_post(c.post),
        'created_at': c.created_at,
        'user': user,
    } for c in comments]

    return {
        'comments': filled,
        "pagination": {
            "is_last": page >= total_pages,
            "total_pages": total_pages,
            "total_entries": total_comments,
        }
    }