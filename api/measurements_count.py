import os
import psycopg2

# haetaan sijainti ja lasketaan mittausten määrä
def get_measurement_count(location_name):
    with psycopg2.connect(dbname=os.getenv('DB'), user=os.getenv('DB_USER'), password=os.getenv('DB_PWD')
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*)
                FROM measurements m
                JOIN sensors s ON m.sensor_id = s.id
                JOIN locations l ON s.location_id = l.id
                WHERE l.name = %s
            """, (location_name,))

            return cur.fetchone()[0]