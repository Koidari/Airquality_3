import os
from datetime import datetime, timedelta
import psycopg2

def get_average_per_parameter(location_name, date):
    start = datetime.fromisoformat(date)
    end = start + timedelta(days=1)

    # Haetaan parametrin nimi, yksikkö ja keskiarvo sijainnille
    with psycopg2.connect(dbname=os.getenv('DB'), user=os.getenv('DB_USER'), password=os.getenv('DB_PWD')
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.name AS parameter_name,p.units, AVG(m.value) AS average
                FROM measurements m
                JOIN sensors s ON m.sensor_id = s.id
                JOIN locations l ON s.location_id = l.id
                JOIN parameters p ON m.parameter_id = p.id
                WHERE l.name = %s
                AND m.measure_date_and_time >= %s
                AND m.measure_date_and_time < %s
                GROUP BY p.name, p.units
            """, (location_name, start, end))

            rows = cur.fetchall()

            return [{"parameter_name": r[0],
                    "units": r[1],
                    "average": round(r[2], 2)
                }
                for r in rows
            ]