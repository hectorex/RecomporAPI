from datetime import datetime
from . import table_registry
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "user" #Criando tabela user

    id: Mapped[int] = mapped_column(init=False, primary_key=True) #definindo ID como PK
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] #pode se repetir 
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now()) #adicionei agr