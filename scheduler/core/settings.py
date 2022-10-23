from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    class Config:
        env_file = '../.env'


class MailingSettings(Settings):
    announcement_periodicity: int = Field(title='Newsletter frequency.')
    scheduler_batch_size: int = Field(title='Batch size of messages sent to the broker.')


class RedisSettings(Settings):
    host: str
    port: int

    class Config:
        env_prefix = 'REDIS_'


redis_config = RedisSettings()


class CelerySettings(Settings):
    name = 'Notifications scheduler'
    broker = f'redis://{redis_config.host}:{redis_config.port}/0'
    backend = f'redis://{redis_config.host}:{redis_config.port}/0'


mailing_settings = MailingSettings()
celery_settings = CelerySettings()
