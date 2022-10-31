import asyncio
from datetime import datetime

from aio_pika.abc import AbstractIncomingMessage
from core.settings import consumer_settings
from mock.user_data import UserMockData
from orjson import orjson
from pamqp.commands import Basic
from src.sender import MessagesSender
from storage.models.models import EmailMessage
from storage.src.saver import MessagesSaver

from broker.base import BaseBroker
from messages.schema.senders import Senders
from messages.schema.statuses import Statuses
from utils.injectors import broker_injector


class Consumer:

    def __init__(self):
        self.broker = None
        self.queue = None
        self.user_data_service = UserMockData()
        self.min_hour = consumer_settings.min_hour
        self.max_hour = consumer_settings.max_hour
        self.sender = MessagesSender()

    @broker_injector()
    def receive_messages(self, broker: BaseBroker, exchange: str, queue: str):
        self.broker = broker
        self.queue = queue
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(broker.receive(queue_name=queue, callback=self.on_message))

    async def on_message(self, message: AbstractIncomingMessage):
        """
        First, check users timezones to not disturb them at night.
        In some cases the field recipients may be empty. It means, that we need to send
        messages to all users. But some of them may not be happy to receive it right now.
        Thus, we get two mailing lists: one for delayed messages (we will send them back
        to the broker) and one for further check.
        """
        message_as_dict = orjson.loads(message.body)

        check_timezone = message_as_dict['check_timezone']
        check_relevance = message_as_dict['check_relevance']
        recipients_to_send = message_as_dict['recipients']

        if check_timezone:
            recipients_to_send, recipients_to_send_back = await self.check_user_settings(recipients_to_send)
            if recipients_to_send_back:
                await self.send_back(message=message_as_dict, recipients=recipients_to_send_back)
        if check_relevance:
            recipients_to_send, recipients_to_cancel = await self.check_relevance(recipients_to_send)
            if recipients_to_cancel:
                await self.cancel_sending(message=message_as_dict, recipients=recipients_to_cancel)

        emails = self.user_data_service.user_email(recipients_to_send)
        await self.send_message_to_user(message=message_as_dict, recipients=emails)

    async def check_user_settings(self, recipients: list) -> tuple[set, dict]:
        # Check users timezones.
        current_hour = datetime.now().hour
        time_differences = self.user_data_service.user_timezone(recipients)

        send_now = {
            user for user, tz in time_differences.items()
            if self.min_hour <= (current_hour + tz) % 24 <= self.max_hour
        }

        send_later = {}
        for user in time_differences.keys() - send_now:
            send_later.setdefault((self.min_hour - (time_differences[user] + current_hour)) % 24, []).append(user)

        return send_now, send_later

    async def check_relevance(self, recipients: set) -> tuple[set, set]:
        # Check if data is still relevant.
        relevant = self.user_data_service.data_relevance(recipients)
        to_cancel = recipients.difference(relevant)

        return relevant, to_cancel

    async def send_back(self, message: dict, recipients: dict) -> None:
        # Send message back to the broker until better times.
        for hour, recipients_list in recipients.items():
            message.update({'recipients': recipients_list, 'status': Statuses.POSTPONED})
            sent = None
            min_sleep = 0.1
            while type(sent) is not Basic.Ack:
                sent = await self.broker.send(
                    queue_name=self.queue,
                    message=orjson.dumps(message),
                    expiration=hour,
                )
                type(sent) is Basic.Ack or await asyncio.sleep(min_sleep := min_sleep * 2)

    async def cancel_sending(self, message: dict, recipients: set) -> None:
        # Data is not relevant, newsletter for recipients is canceled.
        data = [
            EmailMessage(
                created_at=message['created_at'],
                updated_at=datetime.now(),
                status=Statuses.CANCELED.name,
                sender=Senders(message['sender']),
                recipient=recipient,
                content=orjson.dumps(message['content'])
            )
            for recipient in recipients
        ]

        MessagesSaver.save(data=data)

    async def send_message_to_user(self, message: dict, recipients: set) -> None:
        # Finally we are ready to send message to users.
        self.sender.send(recipients=recipients, message_to_send=message)
