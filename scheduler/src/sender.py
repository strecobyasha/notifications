"""
Messages sender.
"""

import asyncio
import time

from orjson import orjson
from pamqp.commands import Basic

from broker.base import BaseBroker
from messages.producers.base import BaseMessage


class Sender:

    async def send_one(self, broker: BaseBroker, queue: str, message: BaseMessage) -> None:
        sent = None
        min_sleep = 0.1
        while type(sent) is not Basic.Ack:
            sent = await broker.send(queue, orjson.dumps(message.dict()))
            type(sent) is Basic.Ack or time.sleep(min_sleep := min_sleep * 2)

    async def send_many(self, broker: BaseBroker, queue: str, messages: iter) -> None:
        messages_to_send = list(messages)
        min_sleep = 0.1
        while messages_to_send:
            # Send a batch of messages to the broker. Then get a response and check
            # if there are undelivered messages. Repeat sending only
            # not sent messages until the end of the world.
            res = await self.multiple_messages(broker, queue, messages_to_send)
            messages_to_send = list(
                item[0] for item
                in filter(lambda item: type(item[1]) is not Basic.Ack, zip(messages_to_send, res))
            )
            messages_to_send or time.sleep(min_sleep := min_sleep * 2)

    async def multiple_messages(self, broker: BaseBroker, queue: str, messages: iter) -> list:
        coroutines = [
            broker.send(
                queue_name=queue,
                message=orjson.dumps(message.dict())
            )
            for message in messages
        ]
        return await asyncio.gather(*coroutines, return_exceptions=True)
