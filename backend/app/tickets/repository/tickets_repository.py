from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tickets.exceptions.tickets_not_found import TicketsNotFoundError
from app.tickets.model.tickets_model import TicketsModel, WebhookModel
from app.tickets.schema.tickets_schema import TicketChannel, TicketPriority, TicketsSchema, TicketStatus, TicketUpdateSchema


class TicketsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_tickets(
        self,
        customer_name: str | None = None,
        channel: TicketChannel | None = None,
        status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
    ) -> list[TicketsSchema]:
        stmt = select(TicketsModel)

        if customer_name is not None:
            stmt = stmt.where(TicketsModel.customer_name.ilike(f"%{customer_name}%"))

        if channel is not None:
            stmt = stmt.where(TicketsModel.channel == channel)

        if status is not None:
            stmt = stmt.where(TicketsModel.status == status)

        if priority is not None:
            stmt = stmt.where(TicketsModel.priority == priority)

        result = (await self.session.execute(stmt)).scalars().all()

        return [
            TicketsSchema.model_validate(
                ticket,
            )
            for ticket in result
        ]

    async def get_ticket_by_id(self, ticket_id: int) -> TicketsSchema | None:
        stmt = select(TicketsModel).where(TicketsModel.id == ticket_id)

        result = (await self.session.execute(stmt)).scalars().first()

        return TicketsSchema.model_validate(result) if result else None

    async def update_ticket(self, ticket_id: int, data: TicketUpdateSchema) -> TicketsSchema:
        stmt = select(TicketsModel).where(TicketsModel.id == ticket_id)

        ticket = (await self.session.execute(stmt)).scalars().first()

        if not ticket:
            raise TicketsNotFoundError(ticket_id=ticket_id)

        if data.status is not None:
            ticket.status = data.status

        if data.priority is not None:
            ticket.priority = data.priority

        await self.session.commit()
        await self.session.refresh(ticket)

        return TicketsSchema.model_validate(ticket)

    async def get_webhook_url(self) -> str | None:
        stmt = select(WebhookModel).where(WebhookModel.id == 1)

        webhook = (await self.session.execute(stmt)).scalars().first()

        return webhook.url if webhook else None

    async def add_webhook_url(self, url: str) -> None:
        stmt = select(WebhookModel).where(WebhookModel.id == 1)

        webhook = (await self.session.execute(stmt)).scalars().first()

        if webhook:
            webhook.url = url
        else:
            new_webhook = WebhookModel(id=1, url=url)
            self.session.add(new_webhook)

        await self.session.commit()
