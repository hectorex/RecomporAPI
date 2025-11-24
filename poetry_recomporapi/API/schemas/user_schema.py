from pydantic import BaseModel, EmailStr

class DadosUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False


class DadosSenha(BaseModel):
    user_id: int
    nova_senha: str

    