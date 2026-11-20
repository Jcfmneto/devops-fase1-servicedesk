def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_criar_e_obter(client, payload):
    r = client.post("/tickets", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "aberto" and body["sla_horas"] == 8
    assert client.get(f"/tickets/{body['id']}").json()["titulo"] == payload["titulo"]


def test_validacao_payload(client, payload):
    payload["titulo"] = "abc"
    assert client.post("/tickets", json=payload).status_code == 422


def test_prioridade_invalida(client, payload):
    payload["prioridade"] = "urgentissima"
    assert client.post("/tickets", json=payload).status_code == 422


def test_listar_com_filtro(client, payload):
    client.post("/tickets", json=payload)
    t2 = client.post("/tickets", json=payload).json()
    client.patch(f"/tickets/{t2['id']}/status", json={"status": "em_atendimento"})
    assert len(client.get("/tickets").json()) == 2
    assert [t["id"] for t in client.get("/tickets?status=em_atendimento").json()] == [t2["id"]]


def test_transicao_invalida_retorna_409(client, payload):
    t = client.post("/tickets", json=payload).json()
    r = client.patch(f"/tickets/{t['id']}/status", json={"status": "resolvido"})
    assert r.status_code == 409


def test_404(client):
    assert client.get("/tickets/999").status_code == 404
    assert client.patch("/tickets/999/status", json={"status": "fechado"}).status_code == 404
    assert client.delete("/tickets/999").status_code == 404


def test_remover(client, payload):
    t = client.post("/tickets", json=payload).json()
    assert client.delete(f"/tickets/{t['id']}").status_code == 204
    assert client.get(f"/tickets/{t['id']}").status_code == 404
