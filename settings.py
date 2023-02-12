class Settings:
    API_KEY = ''

    def headers(self, key=None):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key if key else self.API_KEY}'
        }


settings = Settings()
