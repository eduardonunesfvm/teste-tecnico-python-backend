from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_registrar_foco_certo():
    response = client.post(
        "/producao/registrar_foco",
        json={
            "nivel_foco": 5,
            "tempo_minutos": 60,
            "comentario": "Estudei FastAPI",
            "categoria": "estudo"
        }
    )

    assert response.status_code == 201


def test_registrar_foco_nivel_invalido():
    response = client.post(
        "/producao/registrar_foco",
        json={
            "nivel_foco": 10,
            "tempo_minutos": 60,
            "comentario": "Teste",
            "categoria": "estudo"
        }
    )

    assert response.status_code == 422


def test_obter_diagnostico():
    response = client.get(
        "/producao/obter_diagnostico/visualizar"
    )

    assert response.status_code == 200