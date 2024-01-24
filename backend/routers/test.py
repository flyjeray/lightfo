from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dependencies import db_dependency
import models

router = APIRouter(
  prefix="/test"
)

class TestModelPostData(BaseModel):
    value: str

@router.get('/')
def get_all_test_entries(db: db_dependency):
    return db.query(models.TestModel).all()

@router.post('/')
def post_test_entry(data: TestModelPostData, db: db_dependency):
    db_entry = models.TestModel(value=data.value)
    db.add(db_entry)
    db.commit()