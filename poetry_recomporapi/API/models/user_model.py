from .table_registry import table_registry
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import String 


@table_registry.mapped_as_dataclass
class User:
    """
    Entidade de Usuário compatível com o padrão 'auth_user' do Django.
    Mantém a interoperabilidade entre os sistemas Web, Mobile e a API.
    """

    __tablename__ = "auth_user" 

    # Chave primária autoincrementada (id padrão Django)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    
    # Credenciais e Unicidade
    username: Mapped[str] = mapped_column(String(150), unique=True) 
    password: Mapped[str]  
    
    # Informações de Perfil (Opcionais para manter flexibilidade)
    first_name: Mapped[str | None] = mapped_column(String(150), default=None) 
    last_name: Mapped[str | None] = mapped_column(String(150), default=None) 
    email: Mapped[str | None] = mapped_column(default=None)

    # Controle de Acesso e Permissões (RBAC)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    # Auditoria de Acesso e Registro
    last_login: Mapped[datetime | None] = mapped_column(default=None)
    date_joined: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
#ps.: o usuário foi criado assim pois este é o user do projeto Web, ou seja, o usuário padrão do Django.