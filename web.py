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

@cache.memoize(timeout=60 * 5)
def query(page, period):
    page = int(page)

    subquery_size = 50000
    bucket_size = 60 * 10
    query_value  = datetime.now() - timedelta(days=1)

    if period == "today":
        subquery_size = 5000
        bucket_size = 60
        query_value  = datetime.now() - timedelta(days=1)
    elif period == "last-hour":
        subquery_size = 5000
        bucket_size = 1
        query_value  = datetime.now() - timedelta(hours=1)
    elif period == "last-6-hours":
        subquery_size = 5000
        bucket_size = 10
        query_value  = datetime.now() - timedelta(hours=6)

    avg_value = func.avg(SensorData.value).label("value")
    avg_time = func.avg(func.strftime("%s", SensorData.measured_at)).label("measured_at")
    group = func.strftime('%s', SensorData.measured_at) / bucket_size

    subquery = db.session.query(SensorData.id).order_by("measured_at")

    if period != "historical":
        subquery = subquery.filter(SensorData.measured_at >= query_value)

    paginated_subquery = subquery.offset(page * subquery_size).limit(subquery_size)

    query = db.session.query(avg_value, avg_time).filter(SensorData.id.in_(paginated_subquery)).filter(SensorData.sensor_id == 1).group_by(group)

    data = [
        {
            "value": (1024 - value) / 1024,
            "time": time
        } for (value, time) in query.all()
    ]

    return jsonify(data)

@app.route('/api', methods=['GET'])
def api():
    page = request.args.get('page')
    period = request.args.get('period')

    if page is None:
        page = 0
    if period is None:
        period = "historical"

    return query(page, period)

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

@app.route('/')
def dashboard():
    return render_template(
        'dashboard.html',
        sensors=["Humidity"],
        sensor_data=[]
    )

if __name__ == '__main__':
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Sensor, db.session))
    admin.add_view(ModelView(SensorData, db.session))

    db.create_all()
    app.run('0.0.0.0', 8000, debug=True)
