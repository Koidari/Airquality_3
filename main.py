from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from api import measurements, locations, measurements_avg_day
from api.measurements_count import get_measurement_count

app = Flask(__name__)

load_dotenv()

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route('/api/measurements')
def get_measurements():
    location_name = request.args.get('location_name')
    date = request.args.get('date')
    data = measurements.get_measurements(location_name, date)
    return jsonify(data)

@app.route('/api/locations')
def get_locations():
    data = locations.get_all_locations()
    return jsonify(data)

@app.route("/api/measurements/count")
def measurement_count():
    location_name = request.args.get("location_name")
    count = get_measurement_count(location_name)
    return jsonify({"count": count})

@app.route('/api/measurements/average')
def average():
    location_name = request.args.get("location_name")
    date = request.args.get("date")
    data = measurements_avg_day.get_average_per_parameter(location_name, date)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)