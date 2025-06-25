from datetime import datetime
from .table_registry import table_registry
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4 


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users_table" #Criando tabela user

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] #pode se repetir 
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=lambda: str(uuid4())) #definindo ID como PK