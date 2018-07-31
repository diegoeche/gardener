export SENSOR=/dev/ttyUSB0
python sensor_loader.py
FLASK_APP=web.py python -m flask run --host=0.0.0.0
