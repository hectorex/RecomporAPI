from datetime import datetime
from .table_registry import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4


@table_registry.mapped_as_dataclass
class Compostagem:
    __tablename__ = "compostagens_table" #Criando tabela compostagem

    data_inicio: Mapped[str] = mapped_column() #data_compostagem para data_inicio
    peso: Mapped[float] = mapped_column() #quantReduo para peso
    frequencia: Mapped[str] = mapped_column()
    fkComposteira: Mapped[str] = mapped_column(ForeignKey("composteiras_table.id_composteira")) #composteira_id para fkComposteira #definindo composteira_id como FK
    fkUsuario_comp: Mapped[int] = mapped_column(ForeignKey("auth_user.id"))
    id_compostagem: Mapped[str] = mapped_column(primary_key=True, default_factory=lambda: str(uuid4())) #id para id_compostagem #definindo ID como PK 
    #data_pronto: Mapped[str] = mapped_column() #previsao para data_pronto
