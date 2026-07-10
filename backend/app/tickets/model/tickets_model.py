from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db.config import Base
from app.tickets.schema.tickets_schema import TicketChannel, TicketPriority, TicketStatus


class TicketsModel(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    customer_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    channel: Mapped[TicketChannel] = mapped_column(sa.String(20), nullable=False)
    subject: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    status: Mapped[TicketStatus] = mapped_column(sa.String(20), nullable=False)
    priority: Mapped[TicketPriority] = mapped_column(sa.String(20), nullable=False)

    def __repr__(self) -> str:
        return (
            f"<TicketsModel(id={self.id}, created_at={self.created_at}, "
            f"customer_name='{self.customer_name}', channel='{self.channel}', "
            f"subject='{self.subject}', status='{self.status}', "
            f"priority='{self.priority}')>"
        )


class WebhookModel(Base):
    __tablename__ = "webhooks"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<WebhookModel(id={self.id}, url='{self.url}')>"
