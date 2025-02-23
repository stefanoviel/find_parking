from config import config
from sqlalchemy import create_engine

engine = create_engine(
    f'postgresql+psycopg2://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.dbname}'
)

def get_connection():
    return engine.connect()
    