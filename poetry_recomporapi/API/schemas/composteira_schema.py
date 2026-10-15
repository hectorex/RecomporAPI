from pydantic import BaseModel, field_validator
from datetime import date, datetime
from fastapi import HTTPException

class DadosComposteira(BaseModel):  # Classe da composteira
    # Esquema de entrada para registro de uma nova composteira.
    nome: str
    tipo: str
    minhocas: bool
    data_construcao: date  
    regiao: str
    tamanho: str
    fkUsuario: int
    
    @field_validator('data_construcao', mode='before')
    def validar_data_criacao(cls, data):
        # Aceitar string no formato DD-MM-YYYY (padrao brazuca) e converter para date
        if isinstance(data, str): #verificando tipo (is esse tipo)
            try:
                data_verificando = datetime.strptime(data, "%d-%m-%Y").date()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Use o formato DD-MM-YYYY."
                )
        elif isinstance(data, date):
            data_verificando = data
        else:
            raise HTTPException(
                status_code=400,
                detail="Data inválida."
            )
        
        today_date = datetime.today().date()
        if data_verificando > today_date:  # data futura inválida
            raise HTTPException(
                status_code=400,
                detail="Data posterior à data de hoje."
            )
        return data_verificando
