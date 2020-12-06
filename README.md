SmartGardenSystem 2 - Version May 2020 and on<BR>
SwitchDoc Labs<BR>
May 2020<BR>

Version 021 - October 1, 2020 - Added compatiblitly with new WeatherSense WeatherRack2 and Indoor T/H<BR>
Version 020 - September 4, 2020 - Added Orchid Features, small bug fixes<BR>
Version 019 - August 14, 2020 - Added Indoor TH page on dash_app<BR> 
Version 018 - August 13, 2020 - Fixed Manual Valve Activation Log Entry<BR> 
Version 017 - August 12, 2020 - Fixed testMoistureSensors.py problem <BR> 
Version 016 - August 1, 2020 - Fixed Pi4 Rev2 problem - Kludge - just disables Pixels<BR>
Version 014 - July 14, 2020 - First Release Version <BR>
Version 013 - July 13, 2020 - Release Candidate One <BR>
Version 005 - June 5, 2020 - More modifications to dash_app and wireless<BR>
Version 005 - June 3, 2020 - Added GardenCam / WeatherSTEM code<BR>
Version 003 - May 11, 2020 - Added dashboard code<BR>

To see what is happening on the MQTT channels:<BR>
mosquitto_sub -d -t SGS/#

To Install Yourself: (Note:  This is a complicated install.   For beginners and advanced beginners, you are better of buying a configured SD Card from shop.switchdoc.com)<BR>
This is a Python3 program.  All libraries need to be in python3.<BR>


Installation

1) Install MariaDB on Raspberry Pi

2) Read in the SmartGardenSystem.sql file into the database

3) Install python apscheduler<BR>

 sudo pip3 install apscheduler

4) Install dash libraries (there are a bunch of them).

sudo pip3 install dash<BR>
sudo pip3 install dash-bootstrap-components<BR>
sudo pip3 install plotly<BR>

5) Install remi libraries<BR>

sudo pip3 install remi<BR>


Depending on your system, you may have other missing files.   See the information printed out when your SGS2.py software starts and install the missing librarys.
<BR>

Note: Why don't we supply exact installation procedures?  The reason is is they are different for every distribution on the Raspberry Pi and developers are continuously changing them.  

From our customer frenchi, he has summarized installation instructions:

<pre>

I just followed the instructions from Raspberry using the Raspberry Pi imager App -- it reformats the SD Card which simply allow the Pi4 to reload its boot sw.

After sudo apt-get -y update && apt-get -u dist-upgrade

Note I placed all the SDL software in a directory called SwitchDoc :-)

- sudo apt-get clean
- sudo apt-get autoremove
- sudo apt-get install build-essential python3 python3-pip python3-dev python3-smbus git python3-apscheduler
- sudo apt-get install pigpio python3-pigpio i2c-tools
- sudo apt-get install mariadb-server
- sudo apt-get install mosquitto mosquitto-clients
- sudo apt-get install python-imaging-tk libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libopenjp2-7 libtiff5sudo mysql_secure_installation
- sudo apt-get install scons swig
- sudo raspi-config to enable I2C
- sudo i2cdetect -y 1
- sudo pip3 install --upgrade setuptools pip
- sudo pip3 install setuptools --upgrade
- sudo pip3 install i2cdevice
- sudo pip3 install apscheduler adafruit-blinka picamera
- sudo pip3 install mysqlclient paho-mqtt pillow
- sudo pip3 install dash dash-bootstrap-components plotly remi pandas dash_daq
-
- mkdir SwitchDoc
- cd SwitcDoc
- git clone github.com/adafruit/Adafruit_Python_GPIO.git
- cd Adafruit_Python_GPIO
- sudo python3 setup.py install
- cd ~/SwitchDoc
- git clone github.com/switchdoclabs/SDL_Pi_8PixelStrip.git
- cd SDL_Pi_8PixelStrip
- scons
- cd python
- sudo python3 ./setup.py build
- sudo python3 ./setup.py install
- git clone github.com/switchdoclabs/SDL_Pi_SmartGardenSystem2
- cd ~/SwitchDoc
- cd SDL_Pi_SmartGardenSystem2
- sudo mysql -u root < SmartGardenSystem.sql
- sudo python3 SGSConfigure.py
- sudo python3 SSG2.py

</pre>


