from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dependencies import db_dependency
from pydantic import BaseModel
from sqlalchemy import func, desc
from typing import List, Optional
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
    parent_comment: Optional[int]
    post_title: str
    children_comment_amount: int
    created_at: datetime
    user: User

class PostCommentPayload(BaseModel):
    post_id: int
    parent_comment_id: Optional[int] = None
    text: str

@router.post('/add', status_code=201, response_model=Comment, description="Post a comment to a post")
def post_comment(db: db_dependency, payload: PostCommentPayload, creds: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token_data = auth_utils.verify_token_access(creds.credentials)
    
    post = db.query(models.Post).where(models.Post.id == payload.post_id).first()
    user = db.query(models.User).where(models.User.id == token_data.id).first()

    if post and user:
        comment = models.Comment(text=payload.text, post=payload.post_id, user=user.id, parent_comment=payload.parent_comment_id)
        db.add(comment)
        db.commit()
        db.flush()
        return {
            'id': comment.id,
            'text': comment.text,
            'created_at': comment.created_at,
            'post': payload.post_id,
            'post_title': post.title,
            'parent_comment': payload.parent_comment_id,
            'children_comment_amount': 0,
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
        db.delete(comment)
        db.commit()

    return { 'message': 'success' }

class GetCommentsPayload(BaseModel):
    post_id: int
    parent_comment_id: Optional[int] = None
    page: int
    per_page: int

class GetCommentsResponse(BaseModel):
    comments: List[Comment]
    pagination: models.Pagination

@router.post('/', status_code=200, response_model=GetCommentsResponse, description="Get comments for specific post")
def get_comments_for_post(db: db_dependency, payload: GetCommentsPayload):
    if payload.page < 1 or payload.per_page < 1:
        raise HTTPException(status_code=422, detail="Invalid page parameters")

    post = db.query(models.Post).where(models.Post.id == payload.post_id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post is not found")
    
    if payload.parent_comment_id:
        query = db.query(models.Comment).where(models.Comment.parent_comment == payload.parent_comment_id)
    else:
        query = db.query(models.Comment).where(models.Comment.post == payload.post_id).where(models.Comment.parent_comment == None)

    total_comments = query.with_entities(func.count(models.Comment.id)).scalar()
    total_pages = (total_comments + payload.per_page - 1) // payload.per_page
    offset = (payload.page - 1) * payload.per_page

    comments = query.order_by(desc(models.Comment.created_at)).offset(offset).limit(payload.per_page).all()

    users = {}

    def get_user(user_id):
        user = db.query(models.User).where(models.User.id == user_id).first()
        users[user_id] = user 
        return user  
    
    def get_children(comment_id):
        children = db.query(models.Comment).where(models.Comment.parent_comment == comment_id).with_entities(func.count(models.Comment.id)).scalar()
        return children

    filled = [{    
        'id': c.id,
        'text': c.text,
        'post': c.post,
        'post_title': post.title,
        'parent_comment': c.parent_comment,
        'children_comment_amount': get_children(c.id),
        'created_at': c.created_at,
        'user': users[c.user] if c.user in users else get_user(c.user),
    } for c in comments]

    return {
        'comments': filled,
        "pagination": {
            "is_last": payload.page >= total_pages,
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
    
    def get_children(comment_id):
        children = db.query(models.Comment).where(models.Comment.parent_comment == comment_id).with_entities(func.count(models.Comment.id)).scalar()
        return children

    filled = [{    
        'id': c.id,
        'text': c.text,
        'post': c.post,
        'post_title': posts[c.post] if c.post in posts else get_post(c.post),
        'parent_comment': c.parent_comment,
        'children_comment_amount': get_children(c.id),
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