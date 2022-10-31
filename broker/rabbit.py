import asyncio
from typing import Union

import backoff
from aio_pika import DeliveryMode, Message, connect_robust
from aiormq import ChannelInvalidStateError, ConnectionClosed
from pamqp.commands import Basic

from broker.core.settings import backoff_config, broker_settings
from broker.utils.logger import broker_logger


class Rabbit:

    def __init__(self, exchange_name: str, queue_name: str):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queues = {}
        self.exchange_name = exchange_name
        self.queue_name = queue_name

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.prepare())

    async def prepare(self):
        await self.connect()
        await self.create_exchange(self.exchange_name)
        await self.create_queue(self.queue_name)

    @backoff.on_exception(**backoff_config, logger=broker_logger)
    async def connect(self):
        self.connection = await connect_robust(broker_settings.broker_url)
        self.channel = await self.connection.channel()

    async def create_exchange(self, exchange_name: str):
        self.exchange = await self.channel.declare_exchange(name=exchange_name)

    async def create_queue(self, queue_name: str):
        # Create two queues: the main queue and reserve one without consumer, where
        # messages could spend some time, waiting when they are in demand.
        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange=self.exchange.name)

        delayed_queue = await self.channel.declare_queue(
            f'{queue_name}{broker_settings.suffix}',
            durable=True,
            arguments={
                'x-dead-letter-exchange': self.exchange.name,
                'x-dead-letter-routing-key': queue.name,
            })
        await delayed_queue.bind(exchange=self.exchange.name)
        self.queues.update({queue.name: queue, delayed_queue.name: delayed_queue})

    async def send(self, queue_name: str, message: bytes, expiration: int = 0) -> \
            Union[Basic.Ack, Basic.Nack, Basic.Reject, None]:
        # If the expiration param was passed, message will be moved to the delayed queue.
        queue = f'{queue_name}{broker_settings.suffix}' if expiration else queue_name
        try:
            return await self.exchange.publish(
                Message(message, expiration=expiration, delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=self.queues[queue].name,
            )
        except (ConnectionClosed, ChannelInvalidStateError):
            await self.prepare()

    async def receive(self, queue_name: str, callback):
        await self.queues[queue_name].consume(callback, no_ack=True)
        await asyncio.Future()
