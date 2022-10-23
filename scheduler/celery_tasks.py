from celery import Celery
from celery.schedules import crontab
from core.settings import celery_settings, mailing_settings
from manager import Manager

celery = Celery(celery_settings.name, backend=celery_settings.backend, broker=celery_settings.broker)


@celery.task
def announcement():
    manager = Manager()
    manager.announcement()


@celery.task
def user_stats():
    manager = Manager()
    manager.user_stats()


@celery.on_after_configure.connect
def setup_scheduler_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(0, 0, day_of_month=f'1-31/{mailing_settings.mailing_settings.announcement_periodicity}'),
        announcement.s(),
        name='Send announcement',
    )
    sender.add_periodic_task(crontab(0, 0, day_of_month=1), user_stats.s(), name='Send user stats.')
