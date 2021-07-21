#!/bin/bash
export FLASK_APP=/home/pi/Documents/auto_water/web_app.py
source /home/pi/Documents/auto_water/venv/bin/activate
python -u /home/pi/Documents/auto_water/web_app.py & python -u /home/pi/Documents/auto_water/AutoWater.py --save_data= True