from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from filelock import Timeout, FileLock
from sqlalchemy.sql.expression import func, select

import time
import datetime
from datetime import datetime, date, timedelta

import json

from app import *
from gardener import test_positions, irrigate
from gardener_tab import GardenerTab

# @cache.memoize(timeout=60 * 5)
def query(sensor_id, page, period):
    sensor = Sensor.by_id(int(sensor_id))
    max_value = sensor.max_value
    page = int(page)
    if period == None:
        period = "historical"

    bucket = {
        "historical": "1h",
        "today": "5m",
        "last-6-hours": "1m",
        "last-hour": "1s",
    }[period]

    where_clause = {
        "historical":   "time < now()",
        "today":        "time < now() AND time > (now() - 1d)",
        "last-6-hours": "time < now() AND time > (now() - 6h)",
        "last-hour":    "time < now() AND time > (now() - 1h)",
    }[period]

    # SQL Injection: YOLO
    page_size = 100;

    query = client.query(
        """SELECT (1023 - mean(value)) / 1023
        FROM SENSOR_%s
        WHERE %s
        GROUP BY time(%s) LIMIT %s OFFSET %s;
        """ % (sensor_id, where_clause, bucket, page_size, page * page_size)
    )

    if max_value == 1:
        query = client.query(
            """SELECT 1 - mean(value)
               FROM SENSOR_%s
               WHERE %s AND value <= 1 AND value >= 0
               GROUP BY time(%s) LIMIT %s OFFSET %s;
            """ % (sensor_id, where_clause, bucket, page_size, page * page_size)
        )

    dictionary = query.raw

    if 'series' in dictionary:
        data = [
            {
                "value": value,
                "time": time
            } for (time, value) in query.raw['series'][0]['values']
        ]
        return data
    else:
        return []


@app.route('/api/sensor/<sensor_id>', methods=['GET'])
def sensor(sensor_id):
    page = request.args.get('page')
    period = request.args.get('period')

    if page is None:
        page = 0
    if period is None:
        period = "historical"

    return jsonify(query(sensor_id, page, period))


@app.route('/api/sensors', methods=['GET'])
def sensors():
    sensors = Sensor.all()
    data = [
        {
            "name": sensor.name,
            "value": current_value(sensor.id, sensor.max_value)
        } for sensor in sensors
    ]
    return jsonify(data)

@app.route('/api/plants', methods=['GET'])
def plants():
    plants = Plant.all()
    data = [
        {
            "id":    plant.id,
            "name":  plant.name,
            "sensors": [
                {
                    "name": sensor.name,
                    "value": current_value(sensor.id, sensor.max_value)
                } for sensor in plant.sensors()
            ]
        } for plant in plants
    ]
    return jsonify(data)


@app.route('/api/jobs', methods=['GET'])
def jobs():
    data = GardenerTab.all()
    return jsonify(data)


@app.route('/api/jobs', methods=['POST'])
def create_job():
    input_json = request.json
    GardenerTab.create(input_json)
    return jsonify(input_json)


@app.route('/api/jobs/delete/<id>', methods=['POST'])
def delete_job(id):
    GardenerTab.remove_by_id(int(id))
    return jsonify({"status": "ok"})


@app.route('/')
def home():
    plants = Plant.all()
    return render_template(
        'home.html',
        plants=plants
    )

# TODO: DRY
@app.route('/gardener/test_move', methods=['POST'])
def test_move():
    message = "ok" if test_positions() else "locked"
    return jsonify({ "status": message })

@app.route('/gardener/irrigate/<id>', methods=['POST'])
def irrigate_plant(id):
    amount = request.args.get('amount')

    if amount == None:
        amount = 0

    message = "ok" if irrigate(int(id), int(amount)) else "locked"
    return jsonify({ "status": message })


@app.route('/schedule')
def schedule():
    jobs = GardenerTab.all()
    return render_template(
        'schedule.html',
        jobs=jobs
    )

@app.route('/gardener')
def gardener():
    return render_template('gardener.html')


@app.route('/plant/<plant_id>')
def plant(plant_id):
    plant = Plant.by_id(int(plant_id))
    # sensor = Sensor.by_id(int(plant_id))
    return render_template(
        'dashboard.html',
        plant=plant,
        sensors=json.dumps(plant.sensors(), default=default),
        plants=Plant.all(),
        plant_id=plant_id
    )


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)
