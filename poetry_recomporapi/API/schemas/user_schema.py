from pydantic import BaseModel

class DadosUser(BaseModel): #Classe do user
    username: str
    password: str
    email: str

class DadosSenha(BaseModel): #Classe da senha
    user_id: str
    nova_senha: str
    