# 
# 
# configuration file - DO NOT MODIFY!  
# Defaullts and Configuration are read from a JSON file.   SGS.JSON 
# 
SGSVERSION = "" # set in SGS2.py
STATIONHARDWARE =""
import uuid

# JSON Holders
JSONData = {}
SGSConfigurationJSON = {}


#############
# Software Debug
############
SWDEBUG = False
LOCKDEBUG = False 
############
#MySQL Logging and Password Information
############
enable_MySQL_Logging = False
MySQL_Password = "password"
##########
# Mail / Text Configuration
#########
enableMail = False
mailUser = None
mailPassword = None 
notifyAddress = None
fromAddress = None 
enableText = False

#########
# Pixel Support
#########
enablePixel = False

#########
# Solar Configuration
#########
SolarMAX_Present = None
SolarMAX_Type = None

#########
# Weather Configuration
#########
BMP280_Altitude_Meters = None
Sunlight_Gain = None
weather = False
# printing the value of unique MAC 
# address using uuid and getnode() function  
MACADDRESS = hex(uuid.getnode()) 

############
# WeatherSTEM configuration
############

STATIONMAC = MACADDRESS
STATIONHARDWARE=""
USEWEATHERSTEM = None
INTERVAL_CAM_PICS__SECONDS = None
STATIONKEY = None
Camera_Night_Enable = False

############
# WeatherUnderground
############
WeatherUnderground_Present = None
WeatherUnderground_StationID = None
WeatherUnderground_StationKey = None

############
# Blynk configuration
############

USEBLYNK = False 
BLYNK_AUTH = 'xxxxx'
BLYNK_URL = 'http://blynk-cloud.com/'


############
# REST
############

REST_Enable = None

############
# MQTT
############

MQTT_Enable = False
MQTT_Server_URL = None
MQTT_Port_Number = None
MQTT_Send_Seconds = None


############
# Feature Enable/Disable
############
manual_water = False


############
# Moisture Sensor and Pump Count  - Do not modify
############

moisture_sensor_count = 0
valve_count = 0



# if your pumps stick up too high, adjust this value so tank will still ready empty
Tank_Pump_Level = 15.0
############
#pin defines
############

UltrasonicLevel = 4
pixelPin = 21


############
# device present global variables - DO Not Modify
############


Lightning_Mode = False
Weather_Present = False
GardenCam_Present = False
SunAirPlus_Present = False
SolarMAX_Present = False
OLED_Present = False
BMP280_Present = False

UltrasonicLevel_Present = True

########
#Logging
########

CRITICAL=50
ERROR=40
WARNING=30
INFO=20
JSON=15
DEBUG=10
NOTSET=0


