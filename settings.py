class Settings:
    API_KEY = ''
    FREE_TOKENS = 100

    def headers(self, key=None):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key if key else self.API_KEY}'
        }


settings = Settings()
