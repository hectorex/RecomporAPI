from pydantic import BaseModel, field_validator
from datetime import datetime

class DadosCompostagem(BaseModel):
    nome: str
    data: str
    peso: float
    previsao: int

    @field_validator('data', mode='before')
    def validar_data(cls, data):
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return data
        except ValueError:
            raise ValueError("Use o formato DD/MM/YYYY.")