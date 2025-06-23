import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from API.main import app
from poetry_recomporapi.API.models.user_model import table_registry
'''from sqlalchemy import event
from datetime import datetime
from contextlib import contextmanager'''

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:') #isso esta em memoria, ou seja, isso deixa de existir quando parar de rodar
    
    table_registry.metadata.create_all(engine)

    with Session(engine) as session: # abriu a sessao, o canal de comunicação com o db
        yield session # 'ta aqui o q vc me pediu'

    table_registry.metadata.drop_all(engine)

'''@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 6, 13)): #isso aqui vai servir para configurar a hora do db, configurar apos o celso terminar
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time'''