import uuid


class Settings:
    API_KEY = ''
    FREE_TOKENS = 100
    PASSWORD = uuid.uuid4().hex

    def __init__(self):
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
