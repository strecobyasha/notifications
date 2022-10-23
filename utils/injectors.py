"""
Decorator that defines broker for Api, Admin Panel, Scheduler and Worker.

"""


import functools

from broker.rabbit import Rabbit


def broker_injector(exchange: str = None, queue: str = None):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            exchange_name = exchange or kwargs.get('exchange')
            queue_name = queue or kwargs.get('queue')
            return func(*args, broker=Rabbit(exchange_name=exchange_name, queue_name=queue_name), **kwargs)

        return wrapper

    return inner
