from pydantic import BaseModel, field_validator
from datetime import datetime

class DadosCompostagem(BaseModel):
    nome: str
    data_compostagem: str
    quantReduo: float
    frequencia: str

    @field_validator('data', mode='before')
    def validar_data(cls, data_compostagem):
        try:
            datetime.strptime(data_compostagem, "%d/%m/%Y")
            return data_compostagem
        except ValueError:
            raise ValueError("Use o formato DD/MM/YYYY.")
        
    def calculo_previsao(quantReduo: float) -> int:
        dias = int(quantReduo / 0.5)
        return max(dias, 120) #a cada 500g (0,5kg) leva 1 dia, minimo de 7 dias
        # ele vai retornar isso numa futura rota de post
