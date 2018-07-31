from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import *
import datetime
import json

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))

@app.route('/')
def dashboard():
    query = SensorData.query.all()
    values = [(1024 - sd.value) / 1024 for sd in query]
    times  = [int(sd.measured_at.strftime("%s")) for sd in query]
    size = len(query)/1000
    values = [sum(chunk)/float(len(chunk)) for chunk in chunks(values, size)]
    times = [sum(chunk)/float(len(chunk)) for chunk in chunks(times, size)]

    data = [{"value": value,
             "time": time } for (value, time) in zip(values, times)]

    return render_template(
        'dashboard.html',
        sensors=["Humidity"],
        sensor_data=data
    )

if __name__ == '__main__':
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Sensor, db.session))
    admin.add_view(ModelView(SensorData, db.session))

    db.create_all()
    app.run('0.0.0.0', 8000, debug=True)
