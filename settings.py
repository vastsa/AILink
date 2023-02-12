import uuid


class Settings:
    API_KEY = ''
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
