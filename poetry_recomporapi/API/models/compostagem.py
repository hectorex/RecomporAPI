from datetime import datetime
from .table_registry import table_registry
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4


@table_registry.mapped_as_dataclass
class Compostagem:
    """
    Representação da tabela 'compostagens_table' no banco de dados.
    Utiliza Mapped As Dataclass para facilitar a inicialização e tipagem.
    """
    __tablename__ = "compostagens_table" #Criando tabela compostagem

    # Atributos de dados da compostagem
    data_inicio: Mapped[str] = mapped_column() #data_compostagem para data_inicio
    peso: Mapped[float] = mapped_column() #quantReduo para peso
    frequencia: Mapped[str] = mapped_column()

    # Relacionamentos e Chaves Estrangeiras (FKs)
    # Vincula a compostagem a uma composteira e ao seu criador
    fkComposteira: Mapped[int] = mapped_column(ForeignKey("composteiras_table.id_composteira")) #composteira_id para fkComposteira #definindo composteira_id como FK
    fkUsuario_comp: Mapped[int] = mapped_column(ForeignKey("auth_user.id"))
    
    # Chave Primária (PK) - Gerada automaticamente pelo banco (Serial/Autoincrement)
    # init=False impede que o ID seja exigido no momento da criação do objeto Python
    id_compostagem: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False) #id para id_compostagem #definindo ID como PK 
    
    #data_pronto: Mapped[str] = mapped_column() #previsao para data_pronto NAO APAGAR AINDA
