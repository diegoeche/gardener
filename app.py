from flask import Flask, render_template, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_caching import Cache
from datetime import datetime

import datetime
from datetime import datetime, date, timedelta
from sqlalchemy.sql.expression import func, select

import json

def default(o):
    return o._asdict()

from influxdb import InfluxDBClient

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Check Configuring Flask-Caching section for more details
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': "/home/pi/gardener/cache"})
app.jinja_env.filters['json'] = lambda v: Markup(json.dumps(v))

class Sensor():
    humidity_sensors_count = 12
    all_sensors = [
        {
            "id": id,
            "name": "Humidity %s" % id,
            "max_value": 1 if (id >= 5) else 1024
        } for id in range(1, humidity_sensors_count)
    ]

    all_sensors.append(
        {
            "id": humidity_sensors_count,
            "name": "Light",
            "max_value": 1024
        }
    )
    def __init__(self, attrs):
        self.id = attrs["id"]
        self.name = attrs["name"]
        self.max_value = attrs["max_value"]

    def __repr__(self):
        return "(%s, '%s')" %(self.id, self.name)

    def _asdict(self):
        return {"id": self.id, "name": self.name}

    @staticmethod
    def all():
        return [Sensor(sensor_data) for sensor_data in Sensor.all_sensors]

    @staticmethod
    def by_id(id):
        return Sensor.all()[id - 1]



class Plant():
    all_plants = [
        {
            "id": 1,
            "name": "Basil #1",
            "sensor_ids": [1, 12],
        },
        {
            "id": 2,
            "name": "Parsley #1",
            "sensor_ids": [2, 12],
        },
        {
            "id": 3,
            "name": "Radishes #1",
            "sensor_ids": [3,4,12],
        },
        {
            "id": 4,
            "name": "Radishes #2",
            "sensor_ids": [5,6,12]
        },
    ]

    def __init__(self, attrs):
        self.id = attrs["id"]
        self.name = attrs["name"]
        self.sensor_ids = attrs["sensor_ids"]

    def __repr__(self):
        return "(%s, '%s', %s)" %(self.id, self.name, self.sensors())

    @staticmethod
    def all():
        return [Plant(sensor_data) for sensor_data in Plant.all_plants]

    @staticmethod
    def by_id(id):
        return Plant.all()[id - 1]

    def sensors(self):
        return [Sensor.by_id(sensor_id) for sensor_id in self.sensor_ids]


def ago(delta):
    return datetime.now() - delta

## Refactor me. Use OO
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'gardener_db')

def current_value(sensor_id, max_value):
    if max_value == 1024:
        query = client.query(
        """SELECT (1023 - mean(value)) / 1023
           FROM SENSOR_%s
           WHERE time > now() - 1m
        """ % (sensor_id)
        )
        try:
            return query.raw['series'][0]["values"][0][1]
        except KeyError:
            return 0
    else:
        query = client.query(
        """SELECT 1.0 - mean(value)
           FROM SENSOR_%s
           WHERE time > now() - 1m
        """ % (sensor_id)
        )
        try:
            return query.raw['series'][0]["values"][0][1]
        except KeyError:
            return 0
