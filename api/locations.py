import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Haetaan alasvetovalikolle sijainnit
def get_all_locations():
    with psycopg2.connect(dbname=os.getenv('DB'), user=os.getenv('DB_USER'),password=os.getenv('DB_PWD'),) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            _query = "  SELECT id, name FROM locations"
            cur.execute(_query)
            locations = cur.fetchall()

            return locations