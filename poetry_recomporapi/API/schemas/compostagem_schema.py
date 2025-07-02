from pydantic import BaseModel, field_validator
from datetime import datetime

def calculo_previsao(quantReduo: float) -> int:
        dias = int(quantReduo / 0.5)
        return dias #a cada 500g (0,5kg) leva 1 dia, minimo de 7 dias
        # ele vai retornar isso numa futura rota de post

class DadosCompostagem(BaseModel): #Classe da compostagem
    nome: str
    data_compostagem: str
    quantReduo: float
    frequencia: str
    previsao: int
    composteira_id: str

    @field_validator('data_compostagem', mode='before')
    def validar_data(cls, data_compostagem):
        try:
            datetime.strptime(data_compostagem, "%d/%m/%Y")
            return data_compostagem
        except ValueError:
            raise ValueError("Use o formato DD/MM/YYYY.")
        
    
