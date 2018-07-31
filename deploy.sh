#!/bin/bash
git pull origin master
killall "python -m flask run --host=0.0.0.0"
./start.sh &
