Currently, this project connects to a temperature and humidity sensor on a raspberry pi. It collects data at reguar 
intervals and saves this data in daily files in an s3 bucket. Next I would like to set up a water pump to make my 
plant wet when it gets thirsty

****Requirements****
1. AHT20 sensor
2. Raspberry Pi with Raspbian installed
3. Soldering Iron + solder
4. pin cables for connecting the AHT20 sensor to the raspberry pi


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

5. ```sudo apt-get install libffi-dev libbz2-dev lzma libatlas-base-dev liblzma-dev python3-smbus``` for numpy and pandas to work
6. ```sudo ldconfig```
9. pyenv install 3.7.10
10. Set up remote Interpreter on the raspberry PI using python 3.7.10 and created a new project in pycharm with this remote interpreter
11. Check remote deployment of files in pycharm, check that the folders on each compter are the correct ones

****Set up of virtual enviroment****
1. ```mkdir /home/pi/Documents/auto_water/venv```
2. ```/home/pi/.pyenv/versions/3.7.10/bin/python -m venv /home/pi/Documents/auto_water/venv``` to create the virtual enviroment
3. activate the venv on the remote ```source /home/pi/Documents/auto_water/venv/bin/activate```
4. Install the required packages ```pip3 install -r requirements.txt```


****Setup packages for reading sensor****
1. Enable IC2 on raspberry pi
    ```sudo raspi-config``` -  Then Interfaces anc select the IC2 option, hit activate
   2. ```sudo modprobe i2c_bcm2708```

****Test Sensor****
1. Now run the example.py in the other forked module to see if it starts to read temperatures

****Collect Data****
1. Create a credentials.py file where AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID are set as enviroment variables in os.environ 
   2. Set the output bucket and frequency of data collection in the collect_data script
   3. Run collect_data.py to start collecting data
    
****Set up Pump**** 
1. 





