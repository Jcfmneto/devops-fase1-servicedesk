import pytest

from app.models import Priority, Status, TicketCreate
from app.repository import TicketRepository, TransicaoInvalida


def _novo(repo, prioridade=Priority.media):
    return repo.criar(
        TicketCreate(
            titulo="Sem acesso VPN", descricao="Não consigo conectar na VPN.", solicitante="João", prioridade=prioridade
        )
    )


@pytest.mark.parametrize(
    "prioridade,sla", [(Priority.critica, 4), (Priority.alta, 8), (Priority.media, 24), (Priority.baixa, 72)]
)
def test_sla_calculado_pela_prioridade(prioridade, sla):
    assert _novo(TicketRepository(), prioridade).sla_horas == sla


def test_ids_sequenciais():
    repo = TicketRepository()
    assert [_novo(repo).id for _ in range(3)] == [1, 2, 3]


def test_fluxo_completo_de_status():
    repo = TicketRepository()
    t = _novo(repo)
    for s in (Status.em_atendimento, Status.resolvido, Status.fechado):
        t = repo.atualizar_status(t.id, s)
    assert t.status == Status.fechado and t.atualizado_em is not None


def test_transicao_invalida():
    repo = TicketRepository()
    t = _novo(repo)
    with pytest.raises(TransicaoInvalida):
        repo.atualizar_status(t.id, Status.resolvido)


def test_chamado_fechado_nao_reabre():
    repo = TicketRepository()
    t = _novo(repo)
    repo.atualizar_status(t.id, Status.fechado)
    with pytest.raises(TransicaoInvalida):
        repo.atualizar_status(t.id, Status.aberto)


def test_filtro_por_status():
    repo = TicketRepository()
    a, _ = _novo(repo), _novo(repo)
    repo.atualizar_status(a.id, Status.em_atendimento)
    assert [t.id for t in repo.listar(Status.em_atendimento)] == [a.id]
