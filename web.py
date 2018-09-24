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

    dictionary = query.raw

    if 'series' in dictionary:
        data = [
            {
                "value": value,
                "time": time
            } for (time, value) in query.raw['series'][0]['values']
        ]
        return jsonify(data)
    else:
        return jsonify([])


@app.route('/api/sensor/<sensor_id>', methods=['GET'])
def sensor(sensor_id):
    page = request.args.get('page')
    period = request.args.get('period')

    if page is None:
        page = 0
    if period is None:
        period = "historical"

    return query(sensor_id, page, period)


@app.route('/api/sensors', methods=['GET'])
def sensors():
    sensors = Sensor.query.all()
    data = [
        {
            "name": sensor.name,
            "value": current_value(sensor.id, sensor.max_value)
        } for sensor in sensors
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
    sensors = Sensor.query.all()
    return render_template(
        'home.html',
        sensors=sensors
    )

# TODO: DRY
@app.route('/gardener/test_move', methods=['POST'])
def test_move():
    message = "ok" if test_positions() else "locked"
    return jsonify({ "status": message })

# TODO: make me data-driven
SENSOR_TO_HOSE = {
    "1": 5,
    "2": 2,
    "3": 3,
    "4": 4
}

@app.route('/gardener/irrigate/<id>', methods=['POST'])
def irrigate_plant(id):
    amount = request.args.get('amount')

    if amount == None:
        amount = 0

    message = "ok" if irrigate(SENSOR_TO_HOSE[id], int(amount)) else "locked"
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
    sensor = Sensor.query.filter(Sensor.id == plant_id).one()
    sensors = Sensor.query.all()
    return render_template(
        'dashboard.html',
        sensor=sensor,
        sensors=sensors,
        plant_id=plant_id
    )


if __name__ == '__main__':
    db.create_all()
    app.run('0.0.0.0', 8000, debug=True)
