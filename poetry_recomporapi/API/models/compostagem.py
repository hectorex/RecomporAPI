from datetime import datetime
from .table_registry import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4


@table_registry.mapped_as_dataclass
class Compostagem:
    __tablename__ = "compostagens_table" #Criando tabela compostagem

    nome: Mapped[str] = mapped_column()
    data_compostagem: Mapped[str] = mapped_column()
    quantReduo: Mapped[float] = mapped_column()
    frequencia: Mapped[str] = mapped_column()
    previsao: Mapped[int] = mapped_column() 
    composteira_id: Mapped[str] = mapped_column(ForeignKey("composteiras_table.id")) #definindo composteira_id como FK
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=lambda: str(uuid4())) #definindo ID como PK 