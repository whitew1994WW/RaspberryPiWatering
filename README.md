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


5. pyenv install 3.7.10
6. Set up remote Interpreter on the raspberry PI using python 3.7.10 and created a new project in pycharm with this remote interpreter
7. Check remote deployment of files in pycharm, check that the folders on each compter are the correct ones
8. Set up credentials for aws on the command line

****Set up of virtual enviroment****

1. ```/home/pi/.pyenv/versions/3.7.10/bin/python -m venv /home/pi/Documents/auto_water/``` to create the virtual enviroment
ls
2. activate the venv on the remote ```source /home/pi/Documents/auto_water/venv/bin/activate```
   
****Setup packages for reading sensor****
1. ```sudo apt-get install python3-smbus``` on remote machine
3. Install smbus2 ```pip3 install smbus2```

