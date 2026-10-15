from pydantic import BaseModel, EmailStr

class DadosUser(BaseModel):
    """
    Modelo para criação e gestão de usuários.
    Contém flags de permissão para controle de acesso (RBAC).
    """
    username: str
    password: str
    email: EmailStr
    is_active: bool = True #Define se a conta pode logar no sistema
    is_staff: bool = False #Acesso ao painel administrativo (se houver)
    is_superuser: bool = False #Permissões totais no sistema


class DadosSenha(BaseModel):
    # Esquema para atualização/reset de senha por ID de usuário.
    user_id: int
    nova_senha: str

    