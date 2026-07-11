import asyncio
from collections.abc import Callable
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.shared.db.config import Base
from app.tickets.exceptions.tickets_not_found import TicketsNotFoundError
from app.tickets.model.tickets_model import TicketsModel
from app.tickets.repository.tickets_repository import TicketsRepository
from app.tickets.schema.tickets_schema import TicketChannel, TicketPriority, TicketStatus, TicketUpdateSchema


class TestTicketsRepository:
    def setup_method(self) -> None:
        self.session = AsyncMock(spec=AsyncSession)
        self.repository = TicketsRepository(session=self.session)

    def test_get_tickets_returns_schema_list(
        self, ticket_row: SimpleNamespace, execute_result_factory: Callable[..., MagicMock]
    ) -> None:
        self.session.execute.return_value = execute_result_factory(all_result=[ticket_row])

        result = asyncio.run(self.repository.get_tickets())

        assert len(result) == 1
        assert result[0].ticket_id == ticket_row.id

    def test_get_tickets_returns_empty_list_when_no_tickets(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        self.session.execute.return_value = execute_result_factory(all_result=[])

        result = asyncio.run(self.repository.get_tickets())

        assert result == []

    def test_get_tickets_without_filters_has_no_where_clause(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        self.session.execute.return_value = execute_result_factory(all_result=[])

        asyncio.run(self.repository.get_tickets())

        stmt = self.session.execute.call_args.args[0]
        assert stmt.whereclause is None

    def test_get_tickets_filters_by_customer_name(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        self.session.execute.return_value = execute_result_factory(all_result=[])

        asyncio.run(self.repository.get_tickets(customer_name="Jane"))

        stmt = self.session.execute.call_args.args[0]
        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "customer_name" in compiled
        assert "Jane" in compiled

    def test_get_tickets_filters_by_channel(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        self.session.execute.return_value = execute_result_factory(all_result=[])

        asyncio.run(self.repository.get_tickets(channel=TicketChannel.EMAIL))

        stmt = self.session.execute.call_args.args[0]
        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "channel" in compiled
        assert TicketChannel.EMAIL.value in compiled

    def test_get_tickets_filters_by_status(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        self.session.execute.return_value = execute_result_factory(all_result=[])

        asyncio.run(self.repository.get_tickets(status=TicketStatus.CLOSED))

        stmt = self.session.execute.call_args.args[0]
        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "status" in compiled
        assert TicketStatus.CLOSED.value in compiled

    def test_get_tickets_filters_by_priority(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        self.session.execute.return_value = execute_result_factory(all_result=[])

        asyncio.run(self.repository.get_tickets(priority=TicketPriority.HIGH))

        stmt = self.session.execute.call_args.args[0]
        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "priority" in compiled
        assert TicketPriority.HIGH.value in compiled

    def test_get_tickets_filters_by_customer_name_ignoring_case(self) -> None:
        async def _run(search_term: str) -> list:
            engine = create_async_engine("sqlite+aiosqlite:///:memory:")

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            session_factory = async_sessionmaker(engine, expire_on_commit=False)

            async with session_factory() as session:
                session.add(
                    TicketsModel(
                        created_at=datetime(2026, 1, 1, tzinfo=UTC),
                        customer_name="Jane Doe",
                        channel=TicketChannel.EMAIL,
                        subject="Ticket subject",
                        status=TicketStatus.OPENED,
                        priority=TicketPriority.LOW,
                    )
                )
                await session.commit()

                result = await TicketsRepository(session=session).get_tickets(customer_name=search_term)

            await engine.dispose()

            return result

        for search_term in ("JANE", "jane", "jAnE doe"):
            result = asyncio.run(_run(search_term))

            assert len(result) == 1
            assert result[0].customer_name == "Jane Doe"

    def test_get_ticket_by_id_returns_schema_when_found(
        self, ticket_row: SimpleNamespace, execute_result_factory: Callable[..., MagicMock]
    ) -> None:
        self.session.execute.return_value = execute_result_factory(first_result=ticket_row)

        result = asyncio.run(self.repository.get_ticket_by_id(1))

        assert result is not None
        assert result.ticket_id == ticket_row.id

    def test_get_ticket_by_id_returns_none_when_not_found(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        self.session.execute.return_value = execute_result_factory(first_result=None)

        result = asyncio.run(self.repository.get_ticket_by_id(999))

        assert result is None

    def test_update_ticket_updates_fields_and_returns_schema(
        self,
        ticket_row: SimpleNamespace,
        ticket_update_data: TicketUpdateSchema,
        execute_result_factory: Callable[..., MagicMock],
    ) -> None:
        self.session.execute.return_value = execute_result_factory(first_result=ticket_row)

        result = asyncio.run(self.repository.update_ticket(1, ticket_update_data))

        assert ticket_row.status == ticket_update_data.status
        assert ticket_row.priority == ticket_update_data.priority
        self.session.commit.assert_awaited_once()
        assert result.status == ticket_update_data.status

    def test_update_ticket_raises_when_not_found(
        self, ticket_update_data: TicketUpdateSchema, execute_result_factory: Callable[..., MagicMock]
    ) -> None:
        self.session.execute.return_value = execute_result_factory(first_result=None)

        with pytest.raises(TicketsNotFoundError):
            asyncio.run(self.repository.update_ticket(999, ticket_update_data))

    def test_get_webhook_url_returns_url_when_exists(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        webhook = SimpleNamespace(id=1, url="https://example.com/webhook")
        self.session.execute.return_value = execute_result_factory(first_result=webhook)

        result = asyncio.run(self.repository.get_webhook_url())

        assert result == "https://example.com/webhook"

    def test_get_webhook_url_returns_none_when_not_exists(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        self.session.execute.return_value = execute_result_factory(first_result=None)

        result = asyncio.run(self.repository.get_webhook_url())

        assert result is None

    def test_add_webhook_url_updates_existing_webhook(self, execute_result_factory: Callable[..., MagicMock]) -> None:
        webhook = SimpleNamespace(id=1, url="https://old.example.com")
        self.session.execute.return_value = execute_result_factory(first_result=webhook)

        asyncio.run(self.repository.add_webhook_url("https://new.example.com"))

        assert webhook.url == "https://new.example.com"
        self.session.add.assert_not_called()
        self.session.commit.assert_awaited_once()

    def test_add_webhook_url_creates_new_webhook_when_none_exists(
        self, execute_result_factory: Callable[..., MagicMock]
    ) -> None:
        self.session.execute.return_value = execute_result_factory(first_result=None)

        asyncio.run(self.repository.add_webhook_url("https://new.example.com"))

        self.session.add.assert_called_once()
        self.session.commit.assert_awaited_once()
