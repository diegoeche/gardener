from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import *
import json

@app.route('/')
def dashboard():
    data = [{"value": (1024 - sd.value) / 1024,
             "time": sd.measured_at.timestamp()} for sd in SensorData.query.all()]

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
