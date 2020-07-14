#!/usr/bin/env python3
#
# Test SGS System and Connectivity to a Wireless Extender
# SwitchDoc Labs
# July 2020

# set SGSEXT_IP to the IP address of your connected Wireless Extender to be tested
# Example:  SGSEXT_IP = "192.168.1.52"
SGSEXT_IP = "192.168.1.2"

import sys, traceback
import os
import time
import config
import datetime
import requests

import subprocess

from  bmp280 import BMP280


def sendCommandToWireless(myIP, myCommand):
        myURL = 'http://'+str(myIP)+'/'+myCommand
        print ("sending REST URL = ", myURL) 
        try:
                req = requests.get(myURL,timeout=30)
                returnJSON = req.json()

        except Exception:
                traceback.print_exc()
                return {} 
        return returnJSON 


def turnOnTimedValve(singleValve):

        myIP = singleValve["ipaddress"]

        myCommand = "setSingleValve?params=admin,"+str(singleValve["ValveNumber"])+",1,"+str(singleValve["OnTimeInSeconds"])
        return sendCommandToWireless(myIP, myCommand)

def turnOnAndReadMoistureSensors():
    sendCommandToWireless(SGSEXT_IP, "enableMoistureSensors?params=admin,1,1,1,1")
    myJSON = sendCommandToWireless(SGSEXT_IP, "readMoistureSensors?params=admin")
    return myJSON

# Main Program
if __name__ == '__main__':


    print("###########################")
    print("Smart Garden System 2 System Test")
    print("###########################")
    print('%s' % datetime.datetime.now())
    print()
    if (SGSEXT_IP == ""):
        print("###########################")
        print("Error: MUST SET SGSEXT_IP to run Wireless Extender test")
        print("###########################")
        exit()
    print("Wireless Extender Address = ", SGSEXT_IP)
    # test connection to Barometer


    ################
    # BMP280 Test
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


    if (config.BMP280_Present == True):
        print("###########################")
        print("BMP280 Present and working")
        print("###########################")
    else:
        print("###########################")
        print("BMP280 NOT PRESENT - Board Fault")
        print("###########################")
    print()
    print()


    print("###########################")
    print("Starting Wireless Extender Test")
    print("###########################")

    # test Connection to Wireless Extender

    singleValve = {}
    singleValve["id"] = "TEST"
    singleValve["ipaddress"] = SGSEXT_IP
    singleValve["OnTimeInSeconds"] = "20"
    singleValve["ValveNumber"] = "1"

    myJSON = turnOnTimedValve(singleValve)

    if (len(myJSON) == 0):
        print("###########################")
        print("Wireless Extender ", SGSEXT_IP)
        print("NOT RESPONDING")
        print("###########################")
    else:
        print("###########################")
        print("Wireless Extender: ", SGSEXT_IP)
        print("Successfuly Responding")
        print("###########################")
        print(myJSON)
        print("###########################")
        myJSON = turnOnAndReadMoistureSensors()
        print("Moisture Sensors:")
        print(myJSON)
        print("###########################")

