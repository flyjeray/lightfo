from fastapi import APIRouter
from database import db_dependency
from pydantic import BaseModel
import models

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

class User(BaseModel):
    id: int
    username: str

@router.get('/{id}', status_code=200, response_model=User, description="Get details about specific User")
def get_user(db: db_dependency, id: int):
    user = db.query(models.User).where(models.User.id == id).first()
    return {
        'id': user.id,
        'username': user.username
    }