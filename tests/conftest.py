import pytest
from fastapi.testclient import TestClient

from app import main
from app.repository import TicketRepository


@pytest.fixture
def client():
    main.repo = TicketRepository()
    return TestClient(main.app)


@pytest.fixture
def payload():
    return {
        "titulo": "Impressora não imprime",
        "descricao": "A impressora do 3º andar não responde desde ontem.",
        "solicitante": "Maria Souza",
        "prioridade": "alta",
    }
