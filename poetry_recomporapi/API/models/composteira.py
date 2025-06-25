from datetime import datetime
from .table_registry import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

@table_registry.mapped_as_dataclass
class Composteira:
    __tablename__ = "composteiras_table" #Criando tabela composteira

    nome: Mapped[str] = mapped_column()
    tipo: Mapped[str] = mapped_column()
    minhocas: Mapped[bool] = mapped_column()
    data_constru: Mapped[str] = mapped_column()
    regiao: Mapped[str] = mapped_column()
    tamanho: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users_table.id")) #definindo user_id como FK
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=lambda: str(uuid4())) #definindo ID como PK
    #default_factory:  toda vez que um novo objeto for criado, esse valor será gerado automaticamente
    #lambda: verifica se o valor gerado (o id) já existe no banco, para não gerar ids iguais