from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TicketChannel(StrEnum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    CHAT = "chat"
    TELEFONE = "telefone"
    INSTAGRAM = "instagram"


class TicketStatus(StrEnum):
    OPENED = "opened"
    CLOSED = "closed"


class TicketPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SuccessResponseSchema(BaseModel):
    message: str


class TicketsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: int = Field(alias="id")
    created_at: datetime
    customer_name: str
    channel: TicketChannel
    subject: str
    status: TicketStatus
    priority: TicketPriority


class TicketSeedSchema(BaseModel):
    created_at: datetime
    customer_name: str
    channel: TicketChannel
    subject: str
    status: TicketStatus
    priority: TicketPriority


class TicketUpdateSchema(BaseModel):
    status: TicketStatus | None = Field(default=None)
    priority: TicketPriority | None = Field(default=None)


class TicketWebhookUrlSchema(BaseModel):
    url: str
