"""
Messages queues.
"""


class BaseClass:

    def __init__(self):
        self.set_prefix()

    def set_prefix(self):
        for item in [
            attr for attr in dir(self)
            if not callable(getattr(self, attr))
               and not attr.startswith('__')
               and not attr == 'prefix'
        ]:
            setattr(self, item, f'{self.prefix}.{item.lower()}')


class ApiQueues(BaseClass):
    SIGN_UP = 'sign_up'


class ApiEmailQueues(ApiQueues):
    prefix = 'email'


class AdminQueues(BaseClass):
    INFO = 'info'


class AdminEmailQueues(AdminQueues):
    prefix = 'email'


class SchedulerQueues(BaseClass):
    ANNOUNCEMENT = 'announcement'
    STATS = 'stats'


class SchedulerEmailQueues(SchedulerQueues):
    prefix = 'email'


api_email_queues = ApiEmailQueues()
admin_email_queues = AdminEmailQueues()
scheduler_email_queues = SchedulerEmailQueues()
