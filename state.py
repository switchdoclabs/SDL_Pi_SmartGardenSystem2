# 
# contains all the state variables for SmartGardenSystem 2
#

# Check for user imports
from builtins import range
from builtins import object

import config

##################
#  English or Metric
##################
# if False, then English
# if True, then Metric
EnglishMetric = False 

##################
# blynk State Variable 
##################

blynkPlantNumberDisplay = 1


##################
# Moisture Sensors
##################
Moisture_Humidity = 100.0

Raw_Moisture_Humidity_Array = []
for i in range(1, config.moisture_sensor_count+1):
    Raw_Moisture_Humidity_Array.append(3400.0)
Moisture_Humidity_Array = []
for i in range(1, config.moisture_sensor_count+1):
    Moisture_Humidity_Array.append(100.0)

#water below this limit
Moisture_Threshold = 60.0   
##################
# Pump State
##################

Pump_Running = False
Pump_Water_Full = False

##################
# Tank State
##################

Tank_Level = 5.0
Tank_Empty_Level = 10.0
Tank_Full_Level = 2.0
Tank_Percentage_Full = 30.0


##################
# Alarm States
##################
Alarm_Temperature = 5.0  
Alarm_Moisture = 60.0
Alarm_Water = False
Alarm_Air_Quality = 10000 
Alarm_Moisture_Sensor_Fault = 15.0

Alarm_Active = True
Alarm_Cancel = False

Alarm_Last_State = False
Is_Alarm_Temperature = False
Is_Alarm_Moisture = False
Is_Alarm_MoistureFault = False
Is_Alarm_AirQuality = False
Is_Alarm_WaterEmpty = False

##################
# Internal States
##################

# apscheduler scheduler
scheduler = None

# run rainbow simulation on LEDs

runRainbow = False

# turn LED display on/off

runLEDs = True
# plant water requests

#-1 means no plant request
Plant_Number_Water_Request = -1   

Plant_Water_Request_Previous = False
Plant_Water_Request = False


######################
# Locks
######################
UpdateStateLock = None

######################
# extenders and device status
######################

deviceStatus = {}

valveStatus = []

valveTimeStates = []

moistureSensorStates =  []

nextMoistureSensorCheck = None
######################
#  Blynk State
######################


Last_Event = ""

######################
# MQTT From Wireless Units
######################

WirelessMQTTClient = None
WirelessMQTTClientConnected = False


######################
# Weather State Variables
######################

# FT0300 Invalid Statements
# Invalid data / null / max / min defines


INVALID_DATA_8  =               0x7a          # Invalid value (corresponding to 8bit value)
INVALID_DATA_16 =               0x7ffa        # Invalid value (corresponding to 16bit value)
INVALID_DATA_32 =               0x7ffffffa    # Invalid value (corresponding to 32bit value)

NULL_DATA_8     =               0x7b          # Indicates that the field does not exist
NULL_DATA_16    =               0x7ffb
NULL_DATA_32    =               0x7ffffffb

LOW_DATA_8      =               0x7c          # Means less than the minimum value that can be expressed
LOW_DATA_16     =               0x7ffc
LOW_DATA_32     =               0x7ffffffc

HIGH_DATA_8     =               0x7d          # Means greater than the maximum value that can be expressed
HIGH_DATA_16    =               0x7ffd
HIGH_DATA_32    =               0x7ffffffd

# 0x7e, 0x7f skip


# ===============================================================================
# Maximum and minimum
# ===============================================================================
TEMP_MIN_F      =               0            # -40.0F, offset 40.0F
TEMP_MAX_F      =               1800         # 140.0F, offset 40.0F

HUMI_MIN        =               10           # 10%
HUMI_MAX        =               99           # 99%

WIND_MAX        =               500          # 50.0m/s

RAIN_MAX        =               99999        # 9999.9mm

# JSON state record

StateJSON = ""
# WeatherSTEM info

WeatherSTEMHash = ""

# Weather Variable Sensor Reads

lastMainReading ="Never"
lastIndoorReading = "Never"
previousMainReading = "Never"
previousIndoorReading = "Never"
mainID = ""
insideID = ""
# Weather Variables

OutdoorTemperature = 0.0
OutdoorHumidity = 0.0

IndoorTemperature = 0.0
IndoorHumidity = 0.0

Rain60Minutes = 0.0

SunlightVisible = 0.0
SunlightUVIndex  = 0.0

WindSpeed = 0
WindGust  = 0
WindDirection  = 0.2
TotalRain  = 0

BarometricTemperature = 0
BarometricPressure = 0
Altitude = 0 
BarometricPressureSeaLevel = 0
BarometricTemperature = 0
barometricTrend = True
pastBarometricReading = 0

AQI = 0.0
Hour24_AQI = 0.0




# status Values

Last_Event = "My Last Event"
EnglishMetric = 0


# Solar Values


batteryVoltage = 0
batteryCurrent = 0
solarVoltage = 0
solarCurrent = 0
loadVoltage = 0
loadCurrent = 0
batteryPower = 0
solarPower = 0
loadPower = 0
batteryCharge = 0
SolarMAXLastReceived = "None"

SolarMaxIndoorTemperature = 0.0
SolarMaxIndoorHumidity = 0.0


def printState():

    print ("-------------")
    print ("Current State")
    print ("-------------")
    print("latest MainSensor Reading=", lastMainReading)
    print("MainDeviceNumber=", mainID)
    print("OutdoorTemperature = ",OutdoorTemperature )
    print("OutdoorHumidity = ", OutdoorHumidity )

    print("latest Indoor Sensor Reading=", lastIndoorReading)
    print("IndoorDeviceNumber=", insideID)
    print("IndoorTemperature = ",IndoorTemperature)
    print("IndoorHumidity = ",  IndoorHumidity )

    print("Rain60Minutes = ",  Rain60Minutes )

    print("SunlightVisible = ",  SunlightVisible )
    print("SunlightUVIndex  = ", SunlightUVIndex  )

    print("WindSpeed = ", WindSpeed)
    print("WindGust  = ",  WindGust )
    print("WindDirection  = ",  WindDirection )
    print("TotalRain  = ", TotalRain  )

    print ("BarometricTemperature = ", BarometricTemperature )
    print ("BarometricPressure = ", BarometricPressure )
    print ("Altitude = ", Altitude )
    print ("BarometricPressureSeaLevel = ", BarometricPressureSeaLevel )
    print ("BarometricTemperature = ", BarometricTemperature )
    print ("barometricTrend =",barometricTrend )
    print ("pastBarometricReading = ", pastBarometricReading )

    print ("AQI = ",  AQI )
    print ("Hour24_AQI = ",  Hour24_AQI )

    print ("-------------")


    
    print ("-------------")


    print ("runRainbow = ", runRainbow )
    print ("flashStrip = ", flashStrip )
    print ("runOLED =", runOLED )
    print ("-------------")



    print ("Last_Event = ", Last_Event )
    print ("EnglishMetric = ", EnglishMetric )
    
    
    print ("-------------")

    print ("batteryVoltage", batteryVoltage )
    print ("batteryCurrent", batteryCurrent)
    print ("solarVoltage", solarVoltage )
    print ("solarCurrent", solarCurrent)
    print ("loadVoltage", loadVoltage)
    print ("loadCurrent", loadCurrent)
    print ("batteryPower", batteryPower)
    print ("solarPower", solarPower)
    print ("loadPower", loadPower)
    print ("batteryCharge", batteryCharge)

    print ("SolarMAX Indoor Temperature", SolarMaxIndoorTemperature)
    print ("SolarMAX Indoor Humidity", SolarMaxIndoorHumidity)
    print ("SolarMAX Last Received", SolarMAXLastReceived)
    print ("-------------")

    print ("-------------")



import threading
buildJSONSemaphore = threading.Semaphore()

