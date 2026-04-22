import os
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor


def get_measurements(sensor_name, date):
    # Muutetaan aika Pythonin luettavaksi ja poistetaan tzinfo
    start = datetime.fromisoformat(date).replace(tzinfo=None)
    # rajataan väli yhdeksi päiväksi
    end = start + timedelta(days=1)
    # Haetaan mittausarvo,pvm ja aika, sijainti, parametrin nimi ja yksikkö
    with psycopg2.connect(dbname=os.getenv('DB'), user=os.getenv('DB_USER'),password=os.getenv('DB_PWD'),) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            _query = """
                SELECT m.value, m.measure_date_and_time, l.name, p.name AS parameter_name, p.units
                FROM measurements m
                JOIN sensors s ON m.sensor_id = s.id
                JOIN locations l ON s.location_id = l.id
                JOIN parameters p ON m.parameter_id = p.id
                WHERE l.name = %s
                AND m.measure_date_and_time >= %s
                AND m.measure_date_and_time < %s
                
            """
            cur.execute(_query, (sensor_name, start, end))


            return cur.fetchall()
