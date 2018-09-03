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

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Check Configuring Flask-Caching section for more details
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': "/home/pi/gardener/cache"})

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.filters['json'] = lambda v: Markup(json.dumps(v))

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128))

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('users', lazy=True))


def ago(delta):
    return datetime.now() - delta

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    sensor = db.relationship('Sensor', backref=db.backref('sensors', lazy=True))
    measured_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    @staticmethod
    def average_value():
        return func.avg(SensorData.value).label("value")

    @staticmethod
    def by_id(query, sensor_id):
        return query.filter(SensorData.sensor_id == sensor_id)

    @staticmethod
    def current_value(sensor_id):
        # Last 10 measurements
        ids = db.session.query(SensorData.id).order_by("measured_at DESC").limit(60 * 10)
        avg = SensorData.average_value()
        return SensorData.by_id(db.session.query(avg).filter(SensorData.id.in_(ids)), sensor_id).scalar()

    @staticmethod
    def measured_timestamp():
        return func.strftime("%s", SensorData.measured_at)

    @staticmethod
    def paginated_query(sensor_id, page, period):
        subquery_size = 100000
        bucket_size = 60 * 10

        query_value  = ago(timedelta(days=1))

        if period == "today":
            subquery_size = 20000
            bucket_size = 60
            query_value  = ago(timedelta(days=1))
        elif period == "last-hour":
            subquery_size = 1000
            bucket_size = 1
            query_value  = ago(timedelta(hours=1))
        elif period == "last-6-hours":
            subquery_size = 5000
            bucket_size = 10
            query_value  = ago(timedelta(hours=6))

        avg_value = SensorData.average_value()
        timestamp = SensorData.measured_timestamp()
        avg_time = func.avg(timestamp).label("measured_at")

        subquery = db.session.query(SensorData.id).order_by("measured_at")

        if period != "historical":
            subquery = subquery.filter(SensorData.measured_at >= query_value)

        paginated_subquery = subquery.offset(page * subquery_size).limit(subquery_size)

        filtered_by_id = SensorData.by_id(db.session.query(avg_value, avg_time).filter(SensorData.id.in_(paginated_subquery)), sensor_id)

        return filtered_by_id.group_by(timestamp / bucket_size)
