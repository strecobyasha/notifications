import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.consumer import Consumer

from messages.schema.exchanges import exchanges
from messages.schema.queues import scheduler_email_queues


def receive(exchange: exchanges, queue: scheduler_email_queues):
    consumer = Consumer()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(consumer.receive_messages(exchange=exchange, queue=queue))


if __name__ == '__main__':
    queues = [
        (exchanges.SCHEDULER, scheduler_email_queues.STATS),
        (exchanges.SCHEDULER, scheduler_email_queues.ANNOUNCEMENT),
    ]
    with ThreadPoolExecutor(max_workers=len(queues)) as executor:
        future_to_mapping = [executor.submit(receive, exchange, queue) for exchange, queue in queues]
