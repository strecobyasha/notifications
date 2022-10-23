

class UserMockData:

    def user_timezone(self, users: list) -> dict:
        # Users and time difference relative to server time.
        return {user: 0 for user in users}

    def data_relevance(self, users: set) -> set:
        # Users for whom the data is still relevant.
        return users

    def user_email(self):
        pass
