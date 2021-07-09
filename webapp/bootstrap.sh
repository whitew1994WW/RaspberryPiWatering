#!/bin/sh
export FLASK_APP=/home/pi/Documents/auto_water/webapp/app.py
source /home/pi/Documents/auto_water/venv/bin/activate
flask run -h 0.0.0.0