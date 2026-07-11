import httpx
from fastapi import HTTPException, status

from app.shared.log.logger import logger
from app.tickets.exceptions.tickets_not_found import TicketsNotFoundError
from app.tickets.repository.tickets_repository import TicketsRepository
from app.tickets.schema.tickets_schema import TicketChannel, TicketPriority, TicketsSchema, TicketStatus, TicketUpdateSchema, TicketWebhookUrlSchema


class TicketsService:
    def __init__(self, repository: TicketsRepository, http_client: httpx.Client) -> None:
        self.repository = repository
        self.http_client = http_client

    async def add_webhook_url(self, url: str) -> None:
        try:
            logger.info(f"Adding webhook URL: {url}")
            await self.repository.add_webhook_url(
                url=url,
            )
        except Exception as e:
            logger.exception(f"Error adding webhook URL: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error. Error: {e}",
            ) from e

    async def get_webhook_url(self) -> TicketWebhookUrlSchema:
        try:
            logger.info("Getting webhook URL from repository")
            url = await self.repository.get_webhook_url()

            if not url:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Webhook URL not found.",
                )

            return TicketWebhookUrlSchema(url=url)
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Error getting webhook URL: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error. Error: {e}",
            ) from e

    async def get_tickets(
        self,
        customer_name: str | None = None,
        channel: TicketChannel | None = None,
        status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
    ) -> list[TicketsSchema]:
        logger.info("Getting tickets from repository")

        return await self.repository.get_tickets(
            customer_name=customer_name,
            channel=channel,
            status=status,
            priority=priority,
        )

    async def get_ticket_by_id(self, ticket_id: int) -> TicketsSchema:
        try:
            logger.info(f"Getting ticket with ID: {ticket_id}")

            ticket = await self.repository.get_ticket_by_id(ticket_id=ticket_id)

            if not ticket:
                raise TicketsNotFoundError(ticket_id=ticket_id)

            return ticket
        except TicketsNotFoundError as e:
            logger.error(f"Ticket not found: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with ID {ticket_id} not found.",
            ) from e

        except Exception as e:
            logger.exception(f"Error getting ticket: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error. Error: {e}",
            ) from e

    async def update_ticket(self, ticket_id: int, data: TicketUpdateSchema) -> TicketsSchema:
        try:
            logger.info(f"Updating ticket with ID: {ticket_id}")
            ticket = await self.repository.update_ticket(
                ticket_id=ticket_id,
                data=data,
            )

            if data.status == TicketStatus.CLOSED or data.priority == TicketPriority.HIGH:
                await self._notify_webhook(ticket)

            return ticket
        except TicketsNotFoundError as e:
            logger.error(f"Ticket not found: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with ID {ticket_id} not found.",
            ) from e

        except Exception as e:
            logger.exception(f"Error updating ticket: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error. Error: {e}",
            ) from e

    async def _notify_webhook(self, ticket: TicketsSchema) -> None:
        url = await self.repository.get_webhook_url()

        if not url:
            logger.warning("Webhook URL not found. Skipping webhook notification.")
            return

        response = self.http_client.post(
            url=url,
            json=ticket.model_dump(
                mode="json",
            ),
        )

        if response.status_code != 200:
            logger.error(f"Failed to notify webhook. Status code: {response.status_code}, Response: {response.text}")
