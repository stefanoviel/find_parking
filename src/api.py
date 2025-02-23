
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


@app.route('/api/parks', methods=['GET'])
def get_parks():
    parks = _get_parks()
    return jsonify(parks), 200


def _get_parks() -> List[Dict]:
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