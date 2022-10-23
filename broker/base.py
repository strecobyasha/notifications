from abc import ABC, abstractmethod


class BaseBroker(ABC):

    @abstractmethod
    def send(self, *args, **kwargs):
        """ """

    @abstractmethod
    def receive(self, *args, **kwargs):
        """ """
