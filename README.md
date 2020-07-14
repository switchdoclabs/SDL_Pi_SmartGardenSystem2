SmartGardenSystem 2 - Version May 2020 and on<BR>
SwitchDoc Labs<BR>
May 2020<BR>


Version 014 - July 14, 2020 - First Release Version 
Version 013 - July 13, 2020 - Release Candidate One 
Version 005 - June 5, 2020 - More modifications to dash_app and wireless
Version 005 - June 3, 2020 - Added GardenCam / WeatherSTEM code
Version 003 - May 11, 2020 - Added dashboard code


To Install Yourself: (Note:  This is a complicated install.   For beginners and advanced beginners, you are better of buying a configured SD Card from shop.switchdoc.com)<BR>
This is a Python3 program.  All libraries need to be in python3.<BR>



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
