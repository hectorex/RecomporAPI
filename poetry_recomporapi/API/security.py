from pwdlib import PasswordHash
from uuid import uuid4

pwd_context = PasswordHash.recommended()

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    ...

def password_check(password: str):
    spclCaracs = ["!","@","#","$","%","&","*"]
    strong = True
    if len(password) < 6: 
        strong = False
    elif len(password) > 20:
        strong = False
    elif any(char.isdigit() for char in password) == False:
        strong = False
    elif any(char.isupper() for char in password) == False:
        strong = False
    elif any(char.islower() for char in password) == False:
        strong = False
    elif any(char in spclCaracs for char in password) == False:
        strong = False
    return strong

def username_check(usarname: str):
    spclCaracs = ["!","@","#","$","%","&","*"," "]
    valido = True
    if len(usarname) < 5:
        valido =  False
    elif usarname[0].isalpha() == False:
        valido =  False
    elif any(char in spclCaracs for char in usarname) == True:
        valido = False
    return valido

