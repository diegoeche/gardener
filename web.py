from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import *
import datetime
import json
from  sqlalchemy.sql.expression import func, select

@app.route('/')
def dashboard():
    avg_value = func.avg(SensorData.value).label("value")
    avg_time = func.avg(func.strftime("%s", SensorData.measured_at)).label("measured_at")
    group = func.strftime('%HH-%MM', SensorData.measured_at)
    query = db.session.query(avg_value, avg_time).group_by(group).order_by("measured_at")

    data = [
        {
            "value": (1024 - value) / 1024,
            "time": time
        } for (value, time) in query.all()
    ]

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
