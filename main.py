
from src.db_init_script import load_parking_data, create_park_state_table, create_park_table, initialize_db
from src.api import app, _update_park_state
from dotenv import load_dotenv

if __name__ == '__main__':
    # create_park_table()
    # create_park_state_table()
    # _update_park_state(park_id=207071, state=1)
    # app.run(debug=True)
    # initialize_db()
    load_dotenv(dotenv_path='./.env')
    initialize_db()