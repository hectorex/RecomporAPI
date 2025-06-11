from datetime import datetime
from . import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

@table_registry.mapped_as_dataclass
class Compostagem:
    __tablename__ = "compostagem"

    id: Mapped[int] = mapped_column(init= False, primary_key=True)
    nome: Mapped[str] = mapped_column()
    data_criacao: Mapped[str] = mapped_column()
    peso: Mapped[float] = mapped_column()
    previsao: Mapped[str] = mapped_column(init= False)
    composteira_id: Mapped[int] = mapped_column(ForeignKey("composteira.id"),init= False)
