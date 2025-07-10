from pydantic import BaseModel, field_validator
from datetime import datetime
from fastapi import HTTPException

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
    def validar_data_criacao(cls, data):
        try:
            data_verificando = datetime.strptime(data, "%d-%m-%Y")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Use o formato DD-MM-YYYY.")
        today_date = datetime.today()
        if data_verificando > today_date:  #data recebida é posterior a data de hj (impossível)
            raise HTTPException(
                    status_code=400,
                    detail="Data posterior a de hoje.")
        return data
    
