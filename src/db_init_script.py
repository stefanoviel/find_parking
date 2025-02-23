import geopandas as gpd
from config import config
from src.utils import engine
from sqlalchemy.sql import text


def initialize_db():
    is_initialized = False 
    with engine.connect() as conn:
        result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'park')"))
        is_initialized = result.fetchone()[0]

    if not is_initialized:
        create_park_table()
        create_park_state_table()

def load_parking_data() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(config.path.parking_data)
    gdf = gdf.rename(columns={
        'id1': 'park_id',
        'art': 'park_type',
        'parkdauer': 'park_duration',
        'gebuehrenpflichtig': 'park_charges',
        'geometry': 'geom'
    })
    gdf['park_id'] = gdf['park_id'].astype(int)
    gdf.set_geometry('geom', inplace=True)
    gdf = gpd.GeoDataFrame(gdf[['park_id', 'park_type', 'park_duration', 'park_charges', 'geom']].copy(), crs=gdf.crs, geometry='geom')
    return gdf

def create_park_table():
    park_data = load_parking_data()
    with engine.begin() as conn:
        query = text(f"""
            CREATE TABLE {config.db.tables.park} (
                park_id BIGINT PRIMARY KEY,
                park_type TEXT,
                park_duration DOUBLE PRECISION,
                park_charges TEXT,
                geom GEOMETRY(Point, {park_data.crs.to_epsg()})
            )
        """)
        conn.execute(query)
        park_data.to_postgis(config.db.tables.park, conn, if_exists='append', index=False)


def create_park_state_table():
    with engine.begin() as conn:
        query = text(f"""
            CREATE TABLE {config.db.tables.park_state} (
                park_id BIGINT REFERENCES {config.db.tables.park}(park_id),
                state INTEGER,
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        conn.execute(query)

    

    