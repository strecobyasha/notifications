"""
Models for messages, that were sent via scheduler.
"""

from pydantic import Field

from messages.schema.categories import SchedulerMessageTypes
from messages.schema.senders import Senders

from ..base import BaseMessage
from .content import AnnouncementContent, StatsContent


class SchedulerBaseMessage(BaseMessage):
    sender: Senders = Field(title='Message source', default=Senders.SCHEDULER)


class AnnouncementMessage(SchedulerBaseMessage):
    """ Announcement of the week. """
    group: SchedulerMessageTypes = Field(title='Message group', default=SchedulerMessageTypes.ANNOUNCEMENT)
    template: str = Field(title='Message template', default='base.html')
    content: AnnouncementContent = Field(title='Message content')


class StatsMessage(SchedulerBaseMessage):
    """ User stats. """
    group: SchedulerMessageTypes = Field(title='Message group', default=SchedulerMessageTypes.STATS)
    template: str = Field(title='Message template', default='base.html')
    content: StatsContent = Field(title='Message content')
