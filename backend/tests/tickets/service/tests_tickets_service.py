import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.tickets.exceptions.tickets_not_found import TicketsNotFoundError
from app.tickets.repository.tickets_repository import TicketsRepository
from app.tickets.schema.tickets_schema import TicketPriority, TicketsSchema, TicketStatus, TicketUpdateSchema
from app.tickets.service.tickets_service import TicketsService


class TestTicketsService:
    def setup_method(self) -> None:
        self.repository = AsyncMock(spec=TicketsRepository)
        self.http_client = MagicMock()
        self.service = TicketsService(repository=self.repository, http_client=self.http_client)

    def test_add_webhook_url_calls_repository(self) -> None:
        asyncio.run(self.service.add_webhook_url("https://example.com/webhook"))

        self.repository.add_webhook_url.assert_awaited_once_with(url="https://example.com/webhook")

    def test_add_webhook_url_raises_http_exception_on_error(self) -> None:
        self.repository.add_webhook_url.side_effect = Exception("db down")

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(self.service.add_webhook_url("https://example.com/webhook"))

        assert exc_info.value.status_code == 500

    def test_get_webhook_url_returns_repository_result(self) -> None:
        self.repository.get_webhook_url.return_value = "https://example.com/webhook"

        result = asyncio.run(self.service.get_webhook_url())

        assert result.url == "https://example.com/webhook"

    def test_get_webhook_url_raises_404_when_not_registered(self) -> None:
        self.repository.get_webhook_url.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(self.service.get_webhook_url())

        assert exc_info.value.status_code == 404

    def test_get_webhook_url_raises_500_on_unexpected_error(self) -> None:
        self.repository.get_webhook_url.side_effect = Exception("db down")

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(self.service.get_webhook_url())

        assert exc_info.value.status_code == 500

    def test_get_tickets_returns_repository_result(self, ticket_schema: TicketsSchema) -> None:
        self.repository.get_tickets.return_value = [ticket_schema]

        result = asyncio.run(self.service.get_tickets())

        assert result == [ticket_schema]

    def test_get_tickets_returns_empty_list(self) -> None:
        self.repository.get_tickets.return_value = []

        result = asyncio.run(self.service.get_tickets())

        assert result == []

    def test_update_ticket_skips_webhook_when_not_closed_or_high(
        self, ticket_schema: TicketsSchema, ticket_update_data: TicketUpdateSchema
    ) -> None:
        self.repository.update_ticket.return_value = ticket_schema

        result = asyncio.run(self.service.update_ticket(1, ticket_update_data))

        assert result == ticket_schema
        self.http_client.post.assert_not_called()

    def test_update_ticket_notifies_webhook_when_closed(self, ticket_schema: TicketsSchema) -> None:
        data = TicketUpdateSchema(status=TicketStatus.CLOSED, priority=TicketPriority.LOW)
        self.repository.update_ticket.return_value = ticket_schema
        self.repository.get_webhook_url.return_value = "https://hook.example.com"
        self.http_client.post.return_value = MagicMock(status_code=200)

        asyncio.run(self.service.update_ticket(1, data))

        self.http_client.post.assert_called_once_with(
            url="https://hook.example.com",
            json=ticket_schema.model_dump(mode="json"),
        )

    def test_update_ticket_notifies_webhook_when_high_priority(self, ticket_schema: TicketsSchema) -> None:
        data = TicketUpdateSchema(status=TicketStatus.OPENED, priority=TicketPriority.HIGH)
        self.repository.update_ticket.return_value = ticket_schema
        self.repository.get_webhook_url.return_value = "https://hook.example.com"
        self.http_client.post.return_value = MagicMock(status_code=200)

        asyncio.run(self.service.update_ticket(1, data))

        self.http_client.post.assert_called_once()

    def test_update_ticket_skips_notification_when_no_webhook_url(self, ticket_schema: TicketsSchema) -> None:
        data = TicketUpdateSchema(status=TicketStatus.CLOSED, priority=TicketPriority.LOW)
        self.repository.update_ticket.return_value = ticket_schema
        self.repository.get_webhook_url.return_value = None

        asyncio.run(self.service.update_ticket(1, data))

        self.http_client.post.assert_not_called()

    def test_update_ticket_raises_404_when_ticket_not_found(self, ticket_update_data: TicketUpdateSchema) -> None:
        self.repository.update_ticket.side_effect = TicketsNotFoundError(ticket_id=1)

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(self.service.update_ticket(1, ticket_update_data))

        assert exc_info.value.status_code == 404

    def test_update_ticket_raises_500_on_unexpected_error(self, ticket_update_data: TicketUpdateSchema) -> None:
        self.repository.update_ticket.side_effect = Exception("boom")

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(self.service.update_ticket(1, ticket_update_data))

        assert exc_info.value.status_code == 500
