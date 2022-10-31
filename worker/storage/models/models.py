"""
Models in a history database.
"""

import uuid
from datetime import datetime

from pydantic import BaseSettings, EmailStr, Field


class EmailMessage(BaseSettings):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(title='Creation time')
    updated_at: datetime = Field(title='Last update time')
    status: str = Field(title='Message status')
    sender: str = Field(title='Source of the message')
    recipient: EmailStr = Field(title='Recipient of the message')
    content: bytes = Field(title='Message content')
