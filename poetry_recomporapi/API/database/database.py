#função para parar de repetir toda hora o comando da Session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from API.settings import Settings

engine = create_engine(Settings().DATABASE_URL) # Configuração da Engine: Ponto de entrada da conexão com o banco de dados
session = Session(engine)

def get_session():
    """
    Dependency Injection para sessões do banco de dados.
    Garante que cada requisição tenha sua própria sessão e que
    ela seja fechada (close) automaticamente após o término.
    """
    with Session(engine) as session:
        yield session
    