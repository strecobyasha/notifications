

from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    class Config:
        env_file = '../.env'


class ConsumerSettings(Settings):
    min_hour: int = Field(title='Minimum hour to start newsletter.')
    max_hour: int = Field(title='Maximum hour to start newsletter.')


class SenderSettings(Settings):
    sender_host: str
    sender_port: int
    sender: str


consumer_settings = ConsumerSettings()
sender_settings = SenderSettings()
