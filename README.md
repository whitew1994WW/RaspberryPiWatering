****Initial Setup of Remote Host and Deployment****
1. ssh-copy-id pi@192.168.0.19
2. ssh 'pi@192.168.0.19'
3. password: raspberry and password
curl https://pyenv.run | bash

4. popped this into bash.rc:

	
```
export PATH="/home/pi/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

5. ```sudo apt-get install libffi-dev libbz2-dev lzma libatlas-base-dev liblzma-dev``` for numpy and pandas to work
6. ```sudo ldconfig```
9. pyenv install 3.7.10
10. Set up remote Interpreter on the raspberry PI using python 3.7.10 and created a new project in pycharm with this remote interpreter
11. Check remote deployment of files in pycharm, check that the folders on each compter are the correct ones
12. Set up credentials for aws in enviroment variables (i used a seperate local script called credentials.py where I export the AWS settings)

****Set up of virtual enviroment****
1. ```mkdir /home/pi/Documents/auto_water/venv```
2. ```/home/pi/.pyenv/versions/3.7.10/bin/python -m venv /home/pi/Documents/auto_water/venv``` to create the virtual enviroment
3. activate the venv on the remote ```source /home/pi/Documents/auto_water/venv/bin/activate```


****Setup packages for reading sensor****
1. ```sudo apt-get install python3-smbus``` on remote machine
2. Install smbus2 ```pip3 install smbus2```
3. Enable IC2 on raspberry pi
    ```sudo raspi-config``` -  Then Interfaces ancd IC2 option
   4. ```sudo modprobe i2c_bcm2708```

****Test Sensor****
1. Now run the example.py in the other forked module to see if it starts to read temperatures




