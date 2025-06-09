import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from API.main import app
from API.models.user import table_registry


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

from sqlalchemy import event
from API.models import user

def _mock_db_time():
    def fake_time_hook(mapper, connection, target):
        ...
    event.listen(user, "before_insert", fake_time_hook)