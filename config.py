import os

class PathManager:
    def __init__(self):
        self.parking_data = './data/data.gpkg'

class DBManager:
    class Tables:
        def __init__(self):
            self.park = 'park'
            self.park_state = 'park_state'

    def __init__(self):
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.dbname = os.getenv('POSTGRES_DB')

        print(f'Connecting to {self.host}:{self.port} as {self.user} on database {self.dbname}')

        self.tables = self.Tables()


class Config:
    def __init__(self):
        self.path = PathManager()
        self.db = DBManager()


config = Config()