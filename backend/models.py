from sqlalchemy import Column, Integer, String, ARRAY, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_pw = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    relation = Column(Integer, ForeignKey('user-post-relations.post_id', ondelete="CASCADE"), index=True)

class UserPostRelation(Base):
    __tablename__ = "user-post-relations"
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), index=True)
    post_id = Column(Integer, ForeignKey(Post.id, ondelete="CASCADE"), index=True, primary_key=True)
