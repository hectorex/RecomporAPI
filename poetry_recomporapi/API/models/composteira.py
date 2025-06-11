from datetime import datetime
from . import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

@table_registry.mapped_as_dataclass
class Composteira:
    __tablename__ = "composteira"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column()
    tipo: Mapped[str] = mapped_column()
    minhocas: Mapped[bool] = mapped_column()
    data_constru: Mapped[str] = mapped_column()
    regiao: Mapped[str] = mapped_column()
    tamanho: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
