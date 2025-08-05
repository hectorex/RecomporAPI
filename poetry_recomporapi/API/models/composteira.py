from datetime import datetime
from .table_registry import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

@table_registry.mapped_as_dataclass
class Composteira:
    __tablename__ = "composteiras_table" #Criando tabela composteira

    nome: Mapped[str] = mapped_column()
    tipo: Mapped[str] = mapped_column() # Terra ou Caixa
    minhocas: Mapped[bool] = mapped_column()
    data_construcao: Mapped[str] = mapped_column() #verificar se o tipo bate depois com o pjeto web #alterado de data_constru para data_construcao
    regiao: Mapped[str] = mapped_column()
    tamanho: Mapped[str] = mapped_column() #alterado de float para STR - pequena media ou grande - 
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    fkUsuario: Mapped[str] = mapped_column(ForeignKey("users_table.id")) #alterado de user_id para fkUsuario #definindo user_id como FK
    id_composteira: Mapped[str] = mapped_column(primary_key=True, default_factory=lambda: str(uuid4())) #alterado de id para id_composteira #definindo ID como PK
    #default_factory:  toda vez que um novo objeto for criado, esse valor será gerado automaticamente
    #lambda: verifica se o valor gerado (o id) já existe no banco, para não gerar ids iguais