"""
Creating task for newsletter about next matches.
"""

from messages.producers.scheduler.models import AnnouncementMessage
from messages.schema.statuses import Statuses


class Announcement:

    def __init__(self, service):
        self.service = service

    def create_announcement(self) -> list:
        return self.service.create_announcement()

    def create_message(self) -> AnnouncementMessage:
        return AnnouncementMessage(status=Statuses.PREPARED, content={'matches': self.create_announcement()})
