"""
Messages groups.

"""

from enum import Enum


class ApiMessageTypes(Enum):
    SIGN_UP = 1


class AdminMessageTypes(Enum):
    INFO = 1


class SchedulerMessageTypes(Enum):
    ANNOUNCEMENT = 1
    STATS = 2
