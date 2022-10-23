"""
Models for messages, that were sent via Admin Panel.

"""
from pydantic import Field

from messages.schema.categories import AdminMessageTypes
from messages.schema.senders import Senders

from ..base import BaseMessage


class AdminBaseMessage(BaseMessage):
    sender: Senders = Field(title='Message source', default=Senders.ADMIN)


class InfoMessage(AdminBaseMessage):
    """ Informational message. """
    group: AdminMessageTypes = Field(title='Message group', default=AdminMessageTypes.INFO)
    template: str = Field(title='Message template', default='base.html')
