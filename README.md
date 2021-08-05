Currently, this project connects to 3 sensors on a raspberry pi. It collects data at reguar 
intervals and saves this data in daily files in an s3 bucket. It also waters the plant by simulating rain over a period 
of time. It waters the plant when the soil moisture level drops below a user defined threshold.

There is a also a flask server and website for monitoring. On the flask server you can look
at an interactive plot of the historic sensor values. You can also manually update the sensors from the site.



****Requirements****
1. AHT20 sensor, BH1745 Light sensor, Grow moisture sensor
2. Raspberry Pi with Raspbian installed
3. Soldering Iron + solder
4. pin cables for connecting the sensors to the raspberry pi
5. Pololu Basic SPDT Relay Carrier
6. 5v pump


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
1. Enable IC2 on raspberry pi (run command or run script RaspberryPiSetup.sh)
    ```sudo raspi-config``` -  Then Interfaces anc select the IC2 option, hit activate
    2. ```sudo modprobe i2c_bcm2708```

****Test Sensor****
1. Now run the example.py in the other forked module to see if it starts to read temperatures

****Collect Data****
1. Create a credentials.py file where AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID are set as enviroment variables in os.environ 
   2. Set the output bucket and frequency of data collection in the collect_data script
   3. AutoWater.sh to start the flask server and start collecting data.
    
****Set up Pump**** 
1. Connect the pump to the relay.
2. Connect the relay to one of the Pi's 5v power supplys
3. connect the data line to a pin of your choosing, this will be what activates the pump when it is high
4. update the pin the pump is connected to in the settings.py file.

****Set up AWS****
1. Create the bucket you want to use and another for the Athena output
2. Update the bucket details in settings.py
3. Run the test_save_data script with this bucket to insert example data
4. Run an AWS Glue Crawler to automatically build the table required 

****Set up Camera****
1. Add the following to /boot/config.txt: (or run RaspberryPiSetup.sh)
```# Additional settings:
start_x=1             # essential
gpu_mem=128           # at least, or maybe more if you wish
disable_camera_led=1 ```./







