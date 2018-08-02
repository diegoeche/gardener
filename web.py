from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import *
import datetime
import json
from  sqlalchemy.sql.expression import func, select

@app.route('/api', methods=['GET'])
def api():
    page = request.args.get('page')
    if page is None:
        page = 0
    page = int(page)

    subquery_size = 25000

    bucket_size = (60) * 2
    avg_value = func.avg(SensorData.value).label("value")
    avg_time = func.avg(func.strftime("%s", SensorData.measured_at)).label("measured_at")
    group = func.strftime('%s', SensorData.measured_at) / bucket_size
    subquery = db.session.query(SensorData.id).order_by("measured_at")
    paginated_subquery = subquery.offset(page * subquery_size).limit(subquery_size)
    query = db.session.query(avg_value, avg_time).filter(SensorData.id.in_(paginated_subquery)).group_by(group)

    data = [
        {
            "value": (1024 - value) / 1024,
            "time": time
        } for (value, time) in query.all()
    ]
    return jsonify(data)


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
