from pydantic import BaseModel
from uuid import uuid4
class DadosUser(BaseModel): #Classe do user
    username: str
    password: str
    email: str

class DadosSenha(BaseModel): #Classe da senha
    user_id: uuid4
    nova_senha: str
    