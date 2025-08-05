from pydantic import BaseModel, field_validator
from datetime import datetime
from fastapi import HTTPException

class DadosComposteira(BaseModel): #Classe da composteira
    nome: str
    tipo: str
    minhocas: bool
    data_construcao: str
    regiao: str
    tamanho: str
    user_id: str
    
    @field_validator('data_construcao', mode='before')
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