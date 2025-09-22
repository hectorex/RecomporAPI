#função para parar de repetir toda hora o comando da Session
#iniciando o database
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from API.settings import Settings

engine = create_engine(Settings().DATABASE_URL) #criação da engine
session = Session(engine)

def get_session():
    with Session(engine) as session:
        yield session
    