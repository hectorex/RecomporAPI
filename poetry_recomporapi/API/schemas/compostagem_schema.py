from pydantic import BaseModel, field_validator
from datetime import datetime
from fastapi import HTTPException

def calculo_previsao(quantReduo: float) -> int:
        dias = int(quantReduo / 0.5)
        if dias < 1:
            dias = 1
        return dias #a cada 500g (0,5kg) leva 1 dia, minimo de 7 dias
        # ele vai retornar isso numa futura rota de post

class DadosCompostagem(BaseModel): #Classe da compostagem
    data_inicio: str
    peso: float
    frequencia: str 
    fkComposteira: int
    fkUsuario_comp: int
    # id_compostagem: str nao sei pq ta aq se vai ser atribuido sozinho

    @field_validator('data_inicio', mode='before')
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
    
class DadosCompostagemRetorno(BaseModel): #classe q será o retorno, pis conterá a previsao  
    data_inicio: str
    peso: float
    frequencia: str 
    fkComposteira: str
    fkUsuario_comp: str
    id_compostagem: str
    #data_pronto: str

    
