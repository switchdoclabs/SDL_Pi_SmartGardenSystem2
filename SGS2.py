#!/usr/bin/env python3

#
# Smart Garden System 2
#
# SwitchDoc Labs
#

from __future__ import division
from __future__ import print_function
from builtins import range
from past.utils import old_div

SGSVERSION = "011"

#imports 

import sys, traceback
import os
import RPi.GPIO as GPIO
import time
import threading
import json
import pickle
import picamera
import subprocess

from  bmp280 import BMP280
import SkyCamera
import readJSON

import logging; 
logging.basicConfig(level=logging.ERROR) 

import updateBlynk

#appends
sys.path.append('./SDL_Pi_SSD1306')
sys.path.append('./Adafruit_Python_SSD1306')

from neopixel import *

import pixelDriver


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_SSD1306

import Scroll_SSD1306


import ultrasonicRanger



import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import apscheduler.events

import scanForResources


import config

if (config.enable_MySQL_Logging == True):
            import MySQLdb as mdb

import pclogging

import state

import Valves


import AccessMS

import AccessValves

import weatherSensors

import wiredSensors

#initialization

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

################
# Update State Lock - keeps smapling from being interrupted (like by checkAndWater) - Locks I2C Access
################
state.UpdateStateLock = threading.Lock()

###############
# Pixel Strip  LED
###############

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(pixelDriver.LED_COUNT, pixelDriver.LED_PIN, pixelDriver.LED_FREQ_HZ, pixelDriver.LED_DMA, pixelDriver.LED_INVERT, pixelDriver.LED_BRIGHTNESS, pixelDriver.LED_CHANNEL, pixelDriver.LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()
PixelLock = threading.Lock()


###############
# Flash LED
###############

def blinkLED(pixel, color, times, length):

    if (state.runLEDs == True):
        PixelLock.acquire()

        #if (config.SWDEBUG):
        #    print("N--->Blink LED:%i/%i/%i/%6.2f" % (pixel, color, times, length))

        for x in range(0, times):
            strip.setPixelColor(0, color)
            strip.show()
            time.sleep(length)
	
        strip.setPixelColor(0, Color(0,0,0))
        strip.show()

        PixelLock.release()


    
################
#SSD 1306 setup
################

# OLED SSD_1306 Detection

try:
        RST =27
        display = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
        # Initialize library.
        display.begin()
        display.clear()
        display.display()
        config.OLED_Present = True
        OLEDLock = threading.Lock()
except:
        config.OLED_Present = False
        #print("Smart Garden System must have OLED Present")
        #raise SystemExit



###############
#Ultrasonic Level Test
###############
'''
percentFull = ultrasonicRanger.returnPercentFull()
# check for abort
if (percentFull < 0.0):
    if (config.SWDEBUG):
        print("---->Bad Measurement from Ultrasonic Sensor for Tank Level")
    config.UltrasonicLevel_Present = False
else:
    config.UltrasonicLevel_Present = True
'''

import util

###############
# MQTT Setup for Wireless
###############

import MQTTFunctions




################
# BMP280 Setup 
################

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus, i2c_addr=0x77)

try:
        bmp280 = BMP280(i2c_dev=bus, i2c_addr=0x77)
        config.BMP280_Present = True
except Exception as e: 
        if (config.SWDEBUG):
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            print(traceback.format_exc())

        config.BMP280_Present = False

################
# SkyCamera Setup 
################


#Detect Camera WeatherSTEMHash
try:

    with picamera.PiCamera() as cam:
        if (config.SWDEBUG):
            print("Pi Camera Revision",cam.revision)
        cam.close()
    config.GardenCam_Present = True
except:
    config.GardenCam_Present = False


#############################
# apscheduler setup
#############################
# setup tasks
#############################

def tick():
    print('Tick! The time is: %s' % datetime.datetime.now())


def killLogger():
    state.scheduler.shutdown()
    print("Scheduler Shutdown....")
    exit()


def checkAndWater():


    pass


def ap_my_listener(event):
        if event.exception:
              print(event.exception)
              print(event.traceback)


def returnStatusLine(device, state):

        returnString = device
        if (state == True):
                returnString = returnString + ":   \t\tPresent"
        else:
                returnString = returnString + ":   \t\tNot Present"
        return returnString


#############################
# get and store sensor state
#############################



    

#############################
# Alarm Displays 
#############################
def checkForAlarms():

    pass

def centerText(text,sizeofline):
        textlength = len(text)
        spacesCount = old_div((sizeofline - textlength),2)
        mytext = ""
        if (spacesCount > 0):
                for x in range (0, spacesCount):
                        mytext = mytext + " "
        return mytext+text

#############################
# initialize Smart Garden System
#############################

def initializeSGSPart1():
    print("###############################################")
    print("SGS2 Version "+SGSVERSION+"  - SwitchDoc Labs")
    print("###############################################")
    print("")
    print("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
    print("")
    
    
    
    # read in JSON
    # read in JSON
    readJSON.readJSON("")
    readJSON.readJSONSGSConfiguration("")
    pclogging.systemlog(config.INFO,"SGS Version "+SGSVERSION+" Started")
    pclogging.systemlog(config.JSON,"SGS.JSON Loaded: "+json.dumps(config.JSONData ))
    pclogging.systemlog(config.JSON,"SGSConfigurationJSON.JSON Loaded: "+json.dumps(config.SGSConfigurationJSON ))
    pclogging.systemlog(config.CRITICAL,"No Alarm")
    if (config.GardenCam_Present):
        pclogging.systemlog(config.INFO,"Garden Cam Present")
    else:
        pclogging.systemlog(config.INFO,"Garden Cam NOT Present")
        
    # scan and check for resources
    # get if weather is being used
    config.Weather_Present = readJSON.getJSONValue("weather") 


    pass

def initializeSGSPart2():

        # status reports
    
        print("----------------------")
        print("Local Devices")
        print("----------------------")
        print(returnStatusLine("OLED",config.OLED_Present))
        print(returnStatusLine("BMP280",config.BMP280_Present))
        print(returnStatusLine("DustSensor",config.DustSensor_Present))
        #print(returnStatusLine("Sunlight Sensor",config.Sunlight_Present))
        #print(returnStatusLine("hdc1000 Sensor",config.hdc1000_Present))
        #print(returnStatusLine("Ultrasonic Level Sensor",config.UltrasonicLevel_Present))
    
        print("----------------------")
        print("Checking Wireless SGS Devices")
        print("----------------------")
    
        scanForResources.updateDeviceStatus(True)
        
        # turn off All Valves
        AccessValves.turnOffAllValves()
    
    
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        for single in wirelessJSON:
            print(returnStatusLine(str(single["name"])+" - "+str(single["id"]),state.deviceStatus[str(single["id"])]))
    
   
        # Set up Wireless MQTT Links
        MQTTFunctions.startWirelessMQTTClient()

        # subscribe to IDs
        if (len(wirelessJSON) == 0):
            print("################################")
            print("ERROR")
            print("################################")
            print("No Wireless SGS uinits present - run SGSConfigure.py")
            print("################################")
            exit()

        # wait for connection
        while state.WirelessMQTTClientConnected != True:    #Wait for connection
            time.sleep(0.1)


        # subscribe to IDs

        for single in wirelessJSON:
            topic = "SGS/" + single["id"]
            print("subscribing to ", topic)
            state.WirelessMQTTClient.subscribe(topic)


        print()
    
        print()
        print("----------------------")
        print("Plant / Sensor Counts")
        print("----------------------")
        config.moisture_sensor_count = len(readJSON.getJSONValue("WirelessDeviceJSON"))*4 
        config.valve_count = len(readJSON.getJSONValue("WirelessDeviceJSON"))*8 
        print("Sensor Count: ",config.moisture_sensor_count)
        print("Valve Count: ",config.valve_count)
        print()
        if (config.USEBLYNK):
            updateBlynk.blynkTerminalUpdate( "Sensor Count: %d\n"%config.moisture_sensor_count)
            updateBlynk.blynkTerminalUpdate("Pump Count: %d\n"%config.USB_pump_count)
    
        print("----------------------")
        print("Other Smart Garden System Expansions")
        print("----------------------")
        print(returnStatusLine("Weather",config.Weather_Present))
        print(returnStatusLine("GardenCam",config.GardenCam_Present))
        print(returnStatusLine("SunAirPlus",config.SunAirPlus_Present))
        print(returnStatusLine("SolarMAX",config.SunAirPlus_Present))
        print(returnStatusLine("Lightning Mode",config.Lightning_Mode))
    
        print(returnStatusLine("MySQL Logging Mode",config.enable_MySQL_Logging))
        print()
        print("----------------------")
    
        #Establish WeatherSTEMHash
        if (config.USEWEATHERSTEM == True):
            state.WeatherSTEMHash = SkyCamera.SkyWeatherKeyGeneration(config.STATIONKEY)

    
def initializeScheduler():


    
    
    
        state.scheduler.add_listener(ap_my_listener, apscheduler.events.EVENT_JOB_ERROR)	
    
        # prints out the date and time to console
        state.scheduler.add_job(tick, 'interval', seconds=5*60)
        
        # read wireless sensor package
        print("Before Adding readSensors Job")
        if(config.Weather_Present):
             print("Adding readSensors Job")
	     # start in 10 seconds
             starttime = datetime.datetime.now() + datetime.timedelta(seconds=30)
    
             wsjob = state.scheduler.add_job(weatherSensors.readSensors,run_date=starttime) # run in background
             #weatherSensors.readSensors()

             state.scheduler.add_job(weatherSensors.writeWeatherRecord, 'interval', seconds=15*60)
             state.scheduler.add_job(weatherSensors.writeITWeatherRecord, 'interval', seconds=15*60)
        
        if (config.BMP280_Present):
             wiredSensors.readWiredSensors(bmp280)
             state.scheduler.add_job(wiredSensors.readWiredSensors, 'interval', args=[bmp280 ], seconds = 500) 	
    
        # blink optional life light
        state.scheduler.add_job(blinkLED, 'interval', seconds=5, args=[0,Color(0,0,255),1,0.250])
        
        # blink life light
        state.scheduler.add_job(pixelDriver.statusLEDs, 'interval', seconds=15, args=[strip, PixelLock])
    
    
    
        # check device state
        state.scheduler.add_job(scanForResources.updateDeviceStatus, 'interval', seconds=6*120, args=[False])
        #state.scheduler.add_job(scanForResources.updateDeviceStatus, 'interval', seconds=60, args=[False])
    
    
   
        # sky camera
        if (config.USEWEATHERSTEM):
            if (config.GardenCam_Present):
                state.scheduler.add_job(SkyCamera.takeSkyPicture, 'interval', seconds=int(config.INTERVAL_CAM_PICS__SECONDS))

     # check for force water - note the interval difference with updateState
        #state.scheduler.add_job(forceWaterPlantCheck, 'interval', seconds=8)
        
    
        # check for alarms
        state.scheduler.add_job(checkForAlarms, 'interval', seconds=15)
        #state.scheduler.add_job(checkForAlarms, 'interval', seconds=300)
    
    
        #if (config.USEBLYNK):
        #state.scheduler.add_job(updateBlynk.blynkStateUpdate, 'interval', seconds=60)
    
        # MS sensor Read 
        AccessMS.initMoistureSensors() 
        AccessMS.readAllMoistureSensors()
        
        # MQTT now updates the Moisture Sensor arrays 

        #state.scheduler.add_job(AccessMS.readAllMoistureSensors, 'interval', minutes=15)
    
        # sensor timed water and Timed
        tNow  = datetime.datetime.now()
        # round to the next full hour
        tNow -= datetime.timedelta(minutes = tNow.minute, seconds = tNow.second, microseconds =  tNow.microsecond)
        state.nextMoistureSensorActivate = tNow
        
        state.scheduler.add_job(Valves.valveCheck, 'interval', minutes=1)
    
        # sensor manual water
        state.scheduler.add_job(Valves.manualCheck, 'interval', seconds=15)
    
        if (config.DustSensor_Present):
            #scheduler.add_job(DustSensor.read_AQI, 'interval', seconds=60*5)
            state.scheduler.add_job(DustSensor.read_AQI, 'interval', seconds=60*11)
    
    	
        #init blynk app state
        if (config.USEBLYNK):
            updateBlynk.blynkInit()
    	
    	
        
        
def initializeSGSPart3():

        if (config.SWDEBUG):
            if (config.USEBLYNK):
                print("Blynk Status=", updateBlynk.blynkSGSAppOnline())
                updateBlynk.blynkAlarmUpdate();
    
        state.Last_Event = "SGS Started:"+time.strftime("%Y-%m-%d %H:%M:%S")
    
        if (config.USEBLYNK):
            updateBlynk.blynkEventUpdate()
    
        if (config.OLED_Present):
            if (config.LOCKDEBUG):
                 print("Attempt OLEDLock acquired")
            OLEDLock.acquire()
            if (config.LOCKDEBUG):
                 print("OLEDLock acquired")
    	# display logo
            image = Image.open('SmartPlantPiSquare128x64.ppm').convert('1')
    
            display.image(image)
            display.display()
            time.sleep(3.0)
            display.clear()
    
            Scroll_SSD1306.addLineOLED(display,  ("    Welcome to "))
            Scroll_SSD1306.addLineOLED(display,  ("   Smart Garden "))
            if (config.LOCKDEBUG):
                 print("Attempt OLEDLock released")
            OLEDLock.release()
            if (config.LOCKDEBUG):
                 print("OLEDLock released")
    
        
         
        
        # initialize variables
        #
        state.Pump_Water_Full = False
        
                
    
        checkAndWater()
        checkForAlarms()


def pauseScheduler():

    state.scheduler.print_jobs()

    jobs = state.scheduler.get_jobs()
    print("get_jobs=", jobs)
    state.scheduler.print_jobs()
    for job in jobs:
        state.scheduler.remove_job(job.id)
        
    jobs = state.scheduler.get_jobs()
    print("After get_jobs=", jobs)
    state.scheduler.pause()
    print("After get_jobs=", jobs)
    state.scheduler.print_jobs()
    pass


def restartSGS():
    state.WirelessMQTTClient.disconnect()
    state.WirelessMQTTClient.loop_stop()
    pauseScheduler()
 

    initializeSGSPart1()
    initializeSGSPart2() 
    
    initializeScheduler()       
    state.scheduler.resume()
    print("After resume=" )
    state.scheduler.print_jobs()

    initializeSGSPart3()


    pass
#############################
# main program
#############################

    # Main Program
if __name__ == '__main__':
        

    if (config.SWDEBUG):
        print("Starting pigpio daemon")

    # kill all pigpio instances
    try:
        cmd = [ 'killall', 'pigpiod' ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(output)
        time.sleep(5)
    except:
        #print(traceback.format_exc())
        pass

    cmd = [ '/usr/bin/pigpiod' ]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    print(output)
################
# Dust Sensor Setup 
################
    import DustSensor

    try:
        DustSensor.powerOnDustSensor()
        myData = DustSensor.get_data()
        #print ("data=",myData)
        #myAQI = DustSensor.get_aqi()
        #DustSensor.print_data()
        #print ("AQI=", myAQI)
        DustSensor.powerOffDustSensor()
        config.DustSensor_Present = True
    except:
        DustSensor.powerOffDustSensor()
        config.DustSensor_Present = False

    initializeSGSPart1()
    
    # this is the big exception clause that will turn all pumps off if there is a problem
    try: 

        initializeSGSPart2() 
        state.scheduler = BackgroundScheduler()
    
        initializeScheduler()       

        # start state.scheduler
        state.scheduler.start()
        print("-----------------")
        print("Scheduled Jobs") 
        print("-----------------")
        state.scheduler.print_jobs()
        print("-----------------")


        initializeSGSPart3()
        
        #############
        #  Main Loop
        #############
                
    
    
        while True:
           # check for new JSON files
           if (os.path.exists('NEWJSON') == True):
                # remove file
                print("-----------------------")
                print("New JSON files detected")
                print("SGS2 reloading JSON configuration")
                print("-----------------------")
                os.remove('NEWJSON')
                restartSGS()
                pclogging.systemlog(config.INFO,"Reloading SGS with New JSON")
           else:
                #print("No New JSON Files Detected")
                pass

           time.sleep(10.0)
    		
    
    
    except KeyboardInterrupt:  
        	    # here you put any code you want to run before the program   
        	    # exits when you press CTRL+C  
                print("exiting program") 
        #except:  
        	    # this catches ALL other exceptions including errors.  
        	    # You won't get any error messages for debugging  
        	    # so only use it once your code is working  
                    # print "Other error or exception occurred!"  
      
    finally:  
    	    #time.sleep(5)
            #GPIO.cleanup() # this ensures a clean exit 
            AccessValves.turnOffAllValves()
    	    #saveState()
            state.WirelessMQTTClient.disconnect()
            state.WirelessMQTTClient.loop_stop()
 
            print("done")
