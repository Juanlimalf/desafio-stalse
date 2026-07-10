from collections.abc import Callable
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.tickets.schema.tickets_schema import (
    TicketChannel,
    TicketPriority,
    TicketsSchema,
    TicketStatus,
    TicketUpdateSchema,
)


@pytest.fixture
def ticket_row() -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        customer_name="Jane Doe",
        channel=TicketChannel.EMAIL,
        subject="Ticket subject",
        status=TicketStatus.OPENED,
        priority=TicketPriority.LOW,
    )


@pytest.fixture
def ticket_schema(ticket_row: SimpleNamespace) -> TicketsSchema:
    return TicketsSchema.model_validate(
        ticket_row,
    )


@pytest.fixture
def ticket_update_data() -> TicketUpdateSchema:
    return TicketUpdateSchema(status=TicketStatus.OPENED, priority=TicketPriority.LOW)


@pytest.fixture
def execute_result_factory() -> Callable[..., MagicMock]:
    def _factory(*, all_result: list[object] | None = None, first_result: object | None = None) -> MagicMock:
        scalars = MagicMock()
        scalars.all.return_value = all_result if all_result is not None else []
        scalars.first.return_value = first_result

        result = MagicMock()
        result.scalars.return_value = scalars

        return result

    return _factory
