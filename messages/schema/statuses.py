"""
Message statuses.

PREPARED - ready to send user (message has this status when created).
POSTPONED - if user settings doesn't allow to send message right now.
SENT - message sent to user.
RECEIVED - message received to user.
CANCELED - sending canceled because the data is not already relevance.
FAILED - message was not sent due to error.
"""

from enum import Enum


class Statuses(Enum):
    PREPARED = 1
    POSTPONED = 2
    SENT = 3
    RECEIVED = 4
    CANCELED = 5
    FAILED = 6
