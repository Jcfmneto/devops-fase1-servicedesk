from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"
    critica = "critica"


class Status(str, Enum):
    aberto = "aberto"
    em_atendimento = "em_atendimento"
    resolvido = "resolvido"
    fechado = "fechado"


# Transições de status permitidas (regra de negócio do chamado)
TRANSICOES = {
    Status.aberto: {Status.em_atendimento, Status.fechado},
    Status.em_atendimento: {Status.resolvido, Status.aberto},
    Status.resolvido: {Status.fechado, Status.em_atendimento},
    Status.fechado: set(),
}

# SLA em horas por prioridade
SLA_HORAS = {
    Priority.critica: 4,
    Priority.alta: 8,
    Priority.media: 24,
    Priority.baixa: 72,
}


class TicketCreate(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=120)
    descricao: str = Field(..., min_length=10, max_length=2000)
    solicitante: str = Field(..., min_length=3, max_length=80)
    prioridade: Priority = Priority.media


class StatusUpdate(BaseModel):
    status: Status


class Ticket(TicketCreate):
    id: int
    status: Status = Status.aberto
    sla_horas: int
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    atualizado_em: Optional[datetime] = None
