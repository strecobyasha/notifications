"""
Creating task for newsletter for user stats.

"""

from core.settings import mailing_settings

from messages.producers.scheduler.models import StatsMessage
from messages.schema.statuses import Statuses


class UserStats:

    def __init__(self, service):
        self.service = service
        self.batch_size = mailing_settings.scheduler_batch_size

    def get_stats(self) -> iter:
        stats = self.service.get_stats()
        while True:
            try:
                data = next(stats)
            except StopIteration:
                break
            else:
                start, end, batch = 0, self.batch_size, True
                while batch:
                    yield (batch := data[start:end])
                    start, end = end, end + self.batch_size

    def create_messages(self) -> iter:
        stats_data = self.get_stats()
        while True:
            try:
                yield (
                    StatsMessage(recipients=[item['user_id']], status=Statuses.PREPARED, content=item['content'])
                    for item in next(stats_data)
                )
            except StopIteration:
                break
