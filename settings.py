import uuid


class Settings:
    API_KEY = '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'
    FREE_TOKENS = 100
    PASSWORD = None

    def __init__(self):
        if not self.PASSWORD:
            self.PASSWORD = uuid.uuid4().hex
            print('*' * 50)
            print('Settings init')
            print('Your Password:', self.PASSWORD)
            print('*' * 50)

    def headers(self, key=None):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key if key else self.API_KEY}'
        }


settings = Settings()
