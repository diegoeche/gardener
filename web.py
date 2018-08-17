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
from gardener import move_from_to, hose, pumpWater

def normalize(value):
    return (1023 - value) / 1023

# @cache.memoize(timeout=60 * 5)
def query(sensor_id, page, period):
    page = int(page)
    data = [
        {
            "value": normalize(value),
            "time": time
        } for (value, time) in SensorData.paginated_query(sensor_id, page, period).all()
    ]
    return jsonify(data)


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
            "value": normalize(SensorData.current_value(sensor.id))
        } for sensor in sensors
    ]
    return jsonify(data)

@app.route('/')
def home():
    sensors = Sensor.query.all()
    return render_template(
        'home.html',
        sensors=sensors
    )

@app.route('/gardener/test_move', methods=['POST'])
def test_move():
    lock_path = "/home/pi/gardener/locks/gardener.txt.lock"
    gardener_lock = FileLock(lock_path, timeout=100)
    try:
        gardener_lock.acquire(timeout=0.1)
        move_from_to(0,5)
        return jsonify({ "status": "ok" })
    except Timeout:
        return jsonify({ "status": "locked" })
    finally:
        gardener_lock.release()


@app.route('/gardener/irrigate', methods=['POST'])
def irrigate():
    lock_path = "/home/pi/gardener/locks/gardener.txt.lock"
    gardener_lock = FileLock(lock_path, timeout=100)
    try:
        gardener_lock.acquire(timeout=0.1)
        hose(1)
        pumpWater(10)
        return jsonify({ "status": "ok" })
    except Timeout:
        return jsonify({ "status": "locked" })
    finally:
        gardener_lock.release()


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


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
    # admin = Admin(app)
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Sensor, db.session))
    # admin.add_view(ModelView(SensorData, db.session))

    db.create_all()
    app.run('0.0.0.0', 8000, debug=True)
