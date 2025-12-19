from uuid import uuid4
from passlib.hash import django_pbkdf2_sha256

def get_password_hash(raw_password: str) -> str:
    # Gera hash da senha usando o padrão Django (PBKDF2-SHA256) para compatibilidade.
    return django_pbkdf2_sha256.hash(raw_password) #hash padrão do django, para padronizar com user padrao django


def verify_password(plain_password: str, hashed_password: str):
    # Verifica se a senha em texto plano corresponde ao hash armazenado.
    return django_pbkdf2_sha256.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    # Gera o token JWT para autenticação de usuários.
    ...

def password_check(password: str):
    """
    Valida requisitos de senha forte:
    - Entre 6 e 20 caracteres;
    - Letras maiúsculas, minúsculas, números e caracteres especiais.
    """
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
    """
    Valida o formato do username:
    - Mínimo 5 caracteres;
    - Deve começar com letra;
    - Proíbe caracteres especiais específicos.
    """
    spclCaracs = ["!","@","#","$","%","&","*","."]
    valido = True
    if len(usarname) < 5:
        valido =  False
    elif usarname[0].isalpha() == False:
        valido =  False
    elif any(char in spclCaracs for char in usarname) == True:
        valido = False
    return valido

