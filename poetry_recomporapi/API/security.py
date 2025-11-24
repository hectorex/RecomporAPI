from pwdlib import PasswordHash
from sqlalchemy import select
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from zoneinfo import ZoneInfo
from jwt import DecodeError, encode, decode

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from API.database import get_session
from API.models.user_model import User

#provisório
SECRET_KEY = "flamengo-secreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    #expiração de 30 minutos do token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #encodado
    return encoded_jwt

def password_check(password: str):
    spclCaracs = ["!","@","#","$","%","&","*"]
    strong = True
    if len(password) < 6: 
        strong = False
    if len(password) > 20:
        strong = False
    if any(char.isdigit() for char in password) == False:
        strong = False
    if any(char.isupper() for char in password) == False:
        strong = False
    if any(char.islower() for char in password) == False:
        strong = False
    if any(char in spclCaracs for char in password) == False:
        strong = False
    return strong

def get_current_user(
        session: Session = Depends(get_session),
        token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate":"Bearer"},
    )
    
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_user = payload.get("sub")
        if not subject_user:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    
    user = session.scalar(
        select(User).where(User.username == subject_user)
    )

    if not user:
        raise credentials_exception
    
    return user