from datetime import datetime, timezone
from threading import Lock
from typing import Dict, List, Optional

from app.models import SLA_HORAS, TRANSICOES, Status, Ticket, TicketCreate


class TransicaoInvalida(Exception):
    pass


class TicketRepository:
    """Repositório em memória (na fase 2 será substituído pelo RDS PostgreSQL)."""

    def __init__(self) -> None:
        self._dados: Dict[int, Ticket] = {}
        self._seq = 0
        self._lock = Lock()

    def criar(self, dados: TicketCreate) -> Ticket:
        with self._lock:
            self._seq += 1
            ticket = Ticket(id=self._seq, sla_horas=SLA_HORAS[dados.prioridade], **dados.model_dump())
            self._dados[ticket.id] = ticket
            return ticket

    def listar(self, status: Optional[Status] = None) -> List[Ticket]:
        itens = list(self._dados.values())
        if status:
            itens = [t for t in itens if t.status == status]
        return sorted(itens, key=lambda t: t.id)

    def obter(self, ticket_id: int) -> Optional[Ticket]:
        return self._dados.get(ticket_id)

    def atualizar_status(self, ticket_id: int, novo: Status) -> Optional[Ticket]:
        ticket = self._dados.get(ticket_id)
        if ticket is None:
            return None
        if novo not in TRANSICOES[ticket.status]:
            raise TransicaoInvalida(f"Transição {ticket.status.value} -> {novo.value} não permitida")
        ticket.status = novo
        ticket.atualizado_em = datetime.now(timezone.utc)
        return ticket

    def remover(self, ticket_id: int) -> bool:
        return self._dados.pop(ticket_id, None) is not None
