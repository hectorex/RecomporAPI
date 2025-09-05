from datetime import date, datetime
from .table_registry import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

@table_registry.mapped_as_dataclass
class Composteira:
    __tablename__ = "composteiras_table"  # Criando tabela composteira

    fkUsuario: Mapped[str] = mapped_column(ForeignKey("users_table.id"))
    
    nome: Mapped[str] = mapped_column()
    tipo: Mapped[str] = mapped_column()  # Terra ou Caixa
    minhocas: Mapped[bool] = mapped_column()
    data_construcao: Mapped[date] = mapped_column() #mudamos para date para ficar igual o das meninas
    regiao: Mapped[str] = mapped_column()
    tamanho: Mapped[str] = mapped_column()  # pequena, media ou grande
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    id_composteira: Mapped[str] = mapped_column(primary_key=True, default_factory=lambda: str(uuid4()))
