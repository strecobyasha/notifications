"""
Models for messages, that were sent via Api.

"""
from pydantic import Field, EmailStr

from messages.schema.categories import ApiMessageTypes
from messages.schema.senders import Senders

from ..base import BaseMessage


class ApiBaseMessage(BaseMessage):
    sender: Senders = Field(title='Message source', default=Senders.API)


class SignUpMessage(ApiBaseMessage):
    """ Message after user sign up. """
    group: ApiMessageTypes = Field(title='Message group', default=ApiMessageTypes.SIGN_UP)
    template: str = Field(title='Message template', default='base.html')
