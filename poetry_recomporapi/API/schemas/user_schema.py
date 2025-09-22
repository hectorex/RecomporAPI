from pydantic import BaseModel, EmailStr
from uuid import uuid4

#Schema para criação de User

class DadosUser(BaseModel): #Classe do user
    username: str
    password: str
    email: EmailStr #validar o email se ele eh um email msm

class DadosSenha(BaseModel): #Classe da senha
    user_id: uuid4
    nova_senha: str
    