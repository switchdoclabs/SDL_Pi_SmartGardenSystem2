import time
import state
import config
import AccessValves
import readJSON
import AccessMS
import sys
import json

sys.path.append('./SDL_Pi_Grove4Ch16BitADC/SDL_Adafruit_ADS1x15')
sys.path.append('./SDL_Pi_GroveDigitalExtender')


print ("#####################")
print ("Test Moisture Sensors")
print ("#####################")



# read JSON

readJSON.readJSON("")
readJSON.readJSONSGSConfiguration()
config.enable_MySQL_Logging = False
AccessMS.initMoistureSensors()

while (True):

    AccessMS.readAllMoistureSensors()
    time.sleep(5.0)
