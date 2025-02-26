
from src.utils import engine
from config import config
from flask import Flask, request, jsonify
from sqlalchemy.sql import text
from typing import List, Dict
from src.db_init_script import initialize_db
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
CORS(app) 


@app.route('/api/init_db', methods=['GET'])
def init_db():
    initialize_db()
    return jsonify({"message": "Database initialized"}), 200


@app.route('/api/park_geom', methods=['GET'])
def get_park_geom():
    parks = _get_park_geom()
    return jsonify(parks), 200


def _get_park_geom() -> List[Dict]:
    with engine.connect() as conn:
        # Use ST_AsGeoJSON to convert the POINT geometry to a GeoJSON string
        query = text("""
            SELECT
              park_id,
              park_type,
              park_duration,
              park_charges,
              ST_X(geom) AS lon,
              ST_Y(geom) AS lat
            FROM park
        """)
        result = conn.execute(query)
        rows = result.fetchall()

    # Convert rows into a list of dicts
    parks = []
    for row in rows:
        parks.append({
            "park_id": row.park_id,
            "park_type": row.park_type,
            "park_duration": row.park_duration,
            "park_charges": row.park_charges,
            "lon": row.lon,
            "lat": row.lat
        })

    return parks

@app.route('/api/park_geom_state', methods=['GET'])
def get_park_geom_state():
    parks = _get_park_state_and_geom()
    return jsonify(parks), 200

def _get_park_state_and_geom():
    with engine.connect() as conn:
        query = text("""
         WITH latest_park_state AS (
            SELECT park_id, state, updated_at
            FROM (
                SELECT park_id, state, updated_at, row_number() OVER (PARTITION BY park_id ORDER BY updated_at DESC) AS rn
                FROM park_state
            )
            WHERE rn = 1
        ),
        park_geom_state AS (
            SELECT  park_id, 
                    park_type, 
                    park_duration, 
                    park_charges,
                    ST_X(geom) AS lon,
                    ST_Y(geom) AS lat,
                    CASE WHEN state IS NULL THEN 0
                        WHEN updated_at < (NOW() - INTERVAL '30 minutes') THEN 0
                        WHEN updated_at >= (NOW() - INTERVAL '30 minutes') AND state = 0 THEN 0
                        ELSE 1 
                        END 
                    AS state
            FROM park
            LEFT JOIN latest_park_state
            USING (park_id)
        )
        SELECT *
        FROM park_geom_state
        """)
        result = conn.execute(query)
        rows = result.fetchall()

    parks = []
    for row in rows:
        parks.append({
            "park_id": row.park_id,
            "park_type": row.park_type,
            "park_duration": row.park_duration,
            "park_charges": row.park_charges,
            "lon": row.lon,
            "lat": row.lat,
            "state": row.state
        })

    return parks


@app.route('/api/free_parkings', methods=['GET'])
def get_free_parkings():
    parks = _get_free_parkings()
    return jsonify(parks), 200

def _get_free_parkings():
    with engine.connect() as conn:
        query = text("""
        WITH latest_park_state AS (
            SELECT park_id, state, updated_at
            FROM (
                SELECT park_id, state, updated_at, row_number() OVER (PARTITION BY park_id ORDER BY updated_at DESC) AS rn
                FROM park_state
            )
            WHERE rn = 1
        ),
        park_geom_state AS (
            SELECT  park_id, 
                    park_type, 
                    park_duration, 
                    park_charges,
                    ST_X(geom) AS lon,
                    ST_Y(geom) AS lat,
                    CASE WHEN state IS NULL THEN 0
                        WHEN updated_at < (NOW() - INTERVAL '30 minutes') THEN 0
                        WHEN updated_at >= (NOW() - INTERVAL '30 minutes') AND state = 0 THEN 0
                        ELSE 1 
                        END 
                    AS state
            FROM park
            LEFT JOIN latest_park_state
            USING (park_id)
        ),
        free_parkings AS (
            SELECT *
            FROM park_geom_state
            WHERE state = 1
        )
        SELECT *
        FROM free_parkings
        """)
        result = conn.execute(query)
        rows = result.fetchall()

    parks = []
    for row in rows:
        parks.append({
            "park_id": row.park_id,
            "park_type": row.park_type,
            "park_duration": row.park_duration,
            "park_charges": row.park_charges,
            "lon": row.lon,
            "lat": row.lat
        })

    return parks

@app.route('/api/park_state/<int:park_id>/<int:state>', methods=['POST'])
def update_park_state(park_id, state):
    _update_park_state(park_id, state)
    return jsonify({"message": f"Park {park_id} updated to state {state}"}), 200
    

def _update_park_state(park_id: int, state: int) -> bool:
    with engine.begin() as conn:
        query = text(f"""
            INSERT INTO {config.db.tables.park_state} (park_id, state)
            VALUES (:park_id, :state)
        """)
        conn.execute(query, {"park_id": park_id, "state": state})

    return True