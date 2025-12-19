from datetime import date, datetime
from .table_registry import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

@table_registry.mapped_as_dataclass
class Composteira:
    """
    Entidade representativa das composteiras no banco de dados.
    Armazena configurações físicas e vínculo com o proprietário (User).
    """
    __tablename__ = "composteiras_table"  # Criando tabela composteira

    # Chave Estrangeira: Define a propriedade da composteira
    fkUsuario: Mapped[int] = mapped_column(ForeignKey("auth_user.id"))
    
    # Atributos de identificação e características
    nome: Mapped[str] = mapped_column()
    tipo: Mapped[str] = mapped_column()  # Domínio esperado: 'Terra' ou 'Caixa'
    minhocas: Mapped[bool] = mapped_column()
    data_construcao: Mapped[date] = mapped_column() #mudamos para date para ficar igual o das meninas
    regiao: Mapped[str] = mapped_column()
    tamanho: Mapped[str] = mapped_column()  # Domínio esperado: 'Pequena', 'Media' ou 'Grande'
    
    # Metadados de Auditoria: Gerados automaticamente pelo banco de dados no INSERT
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    # Chave Primária Única
    id_composteira: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
