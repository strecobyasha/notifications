"""
Main file for creating a newsletter.
"""

import asyncio

from mock.mock import MockService
from src.sender import Sender
from tasks.announcement import Announcement
from tasks.user_stats import UserStats

from broker.base import BaseBroker
from messages.schema.exchanges import exchanges
from messages.schema.queues import scheduler_email_queues
from utils.injectors import broker_injector


class Manager:

    def __init__(self):
        self.sender = Sender()

    @broker_injector(exchange=exchanges.SCHEDULER, queue=scheduler_email_queues.ANNOUNCEMENT)
    def announcement(
            self,
            broker: BaseBroker,
            queue: str = scheduler_email_queues.ANNOUNCEMENT,
            service: MockService = MockService(),
    ):
        # Create announcement for the week and send one message to the broker for all users.
        announcement = Announcement(service)
        matches = announcement.create_message()

        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.sender.send_one(broker, queue, matches))

    @broker_injector(exchange=exchanges.SCHEDULER, queue=scheduler_email_queues.STATS)
    def user_stats(
            self,
            broker: BaseBroker,
            queue: str = scheduler_email_queues.STATS,
            service: MockService = MockService(),
    ):
        # Collect user stats and create unique message for each user.
        user_stats = UserStats(service)
        messages = user_stats.create_messages()
        self.send_many(broker, queue, messages)

    def send_many(self, broker: BaseBroker, queue: str, messages: iter) -> None:
        # Sending a group of messages to the broker.
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            try:
                batch = next(messages)
            except StopIteration:
                break
            else:
                loop.run_until_complete(self.sender.send_many(broker, queue, batch))
