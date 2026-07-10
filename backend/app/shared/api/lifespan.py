import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import select

from app.shared.db.config import DatabaseConnection
from app.shared.log.logger import logger
from app.tickets.model.tickets_model import TicketsModel
from app.tickets.schema.tickets_schema import TicketSeedSchema

TICKETS_JSON_PATH = Path(__file__).resolve().parents[3] / "tickets.json"
db_connection = DatabaseConnection()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:

    logger.info("Starting lifespan context...")

    await db_connection.create_all()
    await _seed_tickets()

    yield

    logger.info("Ending lifespan context...")


async def _seed_tickets() -> None:
    async with db_connection.managed_session() as session:
        existing = (await session.scalars(select(TicketsModel).limit(1))).first()
        if existing is not None:
            return

        raw_tickets = json.loads(TICKETS_JSON_PATH.read_text(encoding="utf-8"))
        tickets = [
            TicketSeedSchema.model_validate(
                raw,
            )
            for raw in raw_tickets
        ]

        session.add_all(
            TicketsModel(
                **ticket.model_dump(),
            )
            for ticket in tickets
        )

        await session.commit()

        logger.info(f"Seeded {len(tickets)} tickets from tickets.json")
