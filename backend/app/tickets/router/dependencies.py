from typing import Annotated

import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db.config import DatabaseConnection
from app.shared.http_client.client import get_http_client
from app.tickets.repository.tickets_repository import TicketsRepository
from app.tickets.service.tickets_service import TicketsService

db_session = DatabaseConnection()

SessionDep = Annotated[AsyncSession, Depends(db_session.get_session)]
HttpClientDep = Annotated[httpx.Client, Depends(get_http_client)]


def get_repository(session: SessionDep) -> TicketsRepository:
    return TicketsRepository(
        session=session,
    )


RepoDep = Annotated[TicketsRepository, Depends(get_repository)]


def get_service(repository: RepoDep, http_client: HttpClientDep) -> TicketsService:
    return TicketsService(
        repository=repository,
        http_client=http_client,
    )


ServiceDep = Annotated[TicketsService, Depends(get_service)]
