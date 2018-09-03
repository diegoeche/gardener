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
