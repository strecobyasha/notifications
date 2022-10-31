"""
Base message model.
"""
import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from messages.schema.channels import Channels
from messages.schema.statuses import Statuses


class BaseMessage(BaseModel):
    id: uuid.UUID = Field(title='Message id', default_factory=uuid.uuid4)
    created_at: datetime = Field(title='Creation time', default_factory=datetime.now)
    status_updated_at: datetime = Field(title='Last update time', default_factory=datetime.now)
    channel: Channels = Field(title='Message channel', default=Channels.EMAIL)
    status: Statuses = Field(title='Message status')
    recipients: List[uuid.UUID] = Field(title='List of recipients', default=[])
    content: dict = Field(title='Message content')
    check_timezone: bool = Field(title='Need to check the user\'s time zone', default=True)
    check_relevance: bool = Field(title='Need to check data relevance', default=True)
