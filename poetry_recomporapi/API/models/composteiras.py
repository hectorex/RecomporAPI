from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column,registry

table_registry  = registry()

@table_registry.mapped_as_dataclass
class Composteira:
    __tablename__ = "composteira"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column()
    tipo: Mapped[str] = mapped_column()
    minhocas: Mapped[bool] = mapped_column()
    local_construcao: Mapped[str] = mapped_column()
    data_criacao: Mapped[str] = mapped_column()
    regiao: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now
    )

    