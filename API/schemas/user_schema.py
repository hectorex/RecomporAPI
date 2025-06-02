from pydantic import BaseModel

class DadosUser(BaseModel):
    username: str
    password: str
    email: str

class DadosSenha(BaseModel):
    user_id: str
    nova_senha: str
    