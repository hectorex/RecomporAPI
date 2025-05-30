from fastapi import APIRouter
from schemas.user_schema import DadosUser
from database.fake_db import bd_users

router = APIRouter()