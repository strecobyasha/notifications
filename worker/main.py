from messages.schema.exchanges import exchanges
from messages.schema.queues import scheduler_email_queues
from src.consumer import Consumer


if __name__ == '__main__':
    consumer = Consumer()
    consumer.receive_messages(exchange=exchanges.SCHEDULER, queue=scheduler_email_queues.STATS)
