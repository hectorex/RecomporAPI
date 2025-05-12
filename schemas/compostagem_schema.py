from pydantic import BaseModel, field_validator
from datetime import datetime

class DadosCompostagem(BaseModel):
    nome: str
    data: str
    peso: float
    previsao: int
    
    @field_validator('data')
    @classmethod
    def validar_data(cls,data:str):
        try:
            datetime.strptime(data,"%d/%m/%Y")
            return data
        except ValueError:
            raise ValueError("Use o formato DD/MM/YYYY.")

