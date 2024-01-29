from sqlalchemy import Column, Integer, String
from database import Base

class TestModel(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_pw = Column(String, index=True)