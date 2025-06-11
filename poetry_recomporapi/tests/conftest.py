import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from API.main import app
from API.models.user import table_registry
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
def _mock_db_time(model, time=datetime(2025,6,11)): #entender melhor
    def fake_time_hook(mapper, connection, target):
        print(target)
        breakpoint()
    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)

@pytest.fixture
def mock_db_time():
    return _mock_db_time #deu errado essa bomba'''