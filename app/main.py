import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Response, status

from app.models import Status, StatusUpdate, Ticket, TicketCreate
from app.repository import TicketRepository, TransicaoInvalida

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

app = FastAPI(
    title="Service Desk API",
    version=APP_VERSION,
    description="API de chamados de suporte de TI - projeto DevOps na Prática",
)
repo = TicketRepository()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": APP_VERSION}


@app.post("/tickets", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def criar_ticket(dados: TicketCreate) -> Ticket:
    return repo.criar(dados)


@app.get("/tickets", response_model=List[Ticket])
def listar_tickets(status: Optional[Status] = None) -> List[Ticket]:
    return repo.listar(status)


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def obter_ticket(ticket_id: int) -> Ticket:
    ticket = repo.obter(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return ticket


@app.patch("/tickets/{ticket_id}/status", response_model=Ticket)
def atualizar_status(ticket_id: int, body: StatusUpdate) -> Ticket:
    try:
        ticket = repo.atualizar_status(ticket_id, body.status)
    except TransicaoInvalida as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if ticket is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return ticket


@app.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_ticket(ticket_id: int) -> Response:
    if not repo.remover(ticket_id):
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
