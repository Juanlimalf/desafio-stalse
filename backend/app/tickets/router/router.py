from fastapi import APIRouter

from app.tickets.router.dependencies import ServiceDep
from app.tickets.schema.tickets_schema import (
    SuccessResponseSchema,
    TicketChannel,
    TicketPriority,
    TicketsSchema,
    TicketStatus,
    TicketUpdateSchema,
    TicketWebhookUrlSchema,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/webhook")
async def create_ticket(payload: TicketWebhookUrlSchema, service: ServiceDep) -> SuccessResponseSchema:
    """Recebe a URL do webhook que será chamada quando o status do ticket for
    alterado para 'opened' ou quando a prioridade for alterada para 'high'."""

    await service.add_webhook_url(
        payload.url,
    )

    return SuccessResponseSchema(
        message="url do webhook recebido com sucesso",
    )


@router.get("/webhook")
async def get_webhook(service: ServiceDep) -> TicketWebhookUrlSchema:
    """Retorna a URL do webhook atualmente cadastrada."""

    return await service.get_webhook_url()


@router.get("/")
async def get_all_tickets(
    service: ServiceDep,
    customer_name: str | None = None,
    channel: TicketChannel | None = None,
    status: TicketStatus | None = None,
    priority: TicketPriority | None = None,
) -> list[TicketsSchema]:
    """Retorna todos os tickets cadastrados, podendo ser filtrados por customer_name, channel, status e priority."""

    return await service.get_tickets(
        customer_name=customer_name,
        channel=channel,
        status=status,
        priority=priority,
    )


@router.patch("/{ticket_id}")
async def update_ticket(ticket_id: int, payload: TicketUpdateSchema, service: ServiceDep) -> TicketsSchema | SuccessResponseSchema:
    """Atualiza o status e/ou a prioridade de um ticket existente."""

    return await service.update_ticket(
        ticket_id,
        payload,
    )
