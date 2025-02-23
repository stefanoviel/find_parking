import geopandas as gpd
from config import config
from src.utils import get_connection

def load_parking_data_to_postgis():
    gdf = gpd.read_file(config.path.parking_data)
    con = get_connection()
    gdf.to_postgis(config.db.tables.park, con, if_exists='replace')
    con.close()

