from pydantic import BaseModel, field_validator
from datetime import datetime

class DadosComposteira(BaseModel):
    nome: str
    tipo: str
    minhocas: bool
    local_construcao: str
    data_criacao: str
    regiao: str

    @field_validator('data_criacao')
    @classmethod
    def validar_data(cls,data:str):
        try:
            datetime.strptime(data,"%d/%m/%Y")
            return data
        except ValueError:
            raise ValueError("Use o formato DD/MM/YYYY.")