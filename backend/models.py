from sqlalchemy import Column, Integer, String, ARRAY, DateTime, ForeignKey
from sqlalchemy.sql import func
from pydantic import BaseModel
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_pw = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    posts = Column(ARRAY(Integer), index=True, server_default="{}")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), index=True)
    
class Pagination(BaseModel):
    is_last: bool
    total_entries: int
    total_pages: int
