from fastapi import APIRouter
from fastapi.security import HTTPBearer

router = APIRouter(
  prefix='/posts',
  tags=['Posts']
)

token_auth_scheme = HTTPBearer()

