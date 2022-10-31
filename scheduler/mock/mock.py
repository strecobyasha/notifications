"""
Mocking user and games data service.
"""

import uuid


class MockService:

    def __init__(self, batch_num: int = 2, batch_size: int = 4):
        self.batch_num = batch_num
        self.batch_size = batch_size

    def get_stats(self) -> iter:
        for _ in range(self.batch_num):
            batch = [
                {'content': {'stats': {}}, 'user_id': uuid.uuid4()}
                for _ in range(self.batch_size)
            ]
            yield batch

    def create_announcement(self) -> dict:
        return {}
