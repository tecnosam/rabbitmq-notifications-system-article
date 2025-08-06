from typing import Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Recipient(BaseModel):
    address: str
    name: str

class EmailPayload(BaseModel):
    recipient: Recipient
    subject: str
    body: str
    templateId: str
    data: Dict[str, Any]

class Metadata(BaseModel):
    sourceService: str
    correlationId: UUID = Field(default_factory=uuid4)
    retryCount: int = 0

class NotificationMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    messageRoute: str
    schema: str
    payload: Dict[str, Any]
    metadata: Metadata