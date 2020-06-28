# Scan for SGS Resources

import requests
import json
import ipaddress

import subprocess

import datetime
import traceback
import sys
import time

import config
import readJSON
import state
import socket
import pclogging


def sendCommandToWireless(myIP, myCommand):
        myURL = 'http://'+str(myIP)+'/'+myCommand
        
        try:
                if (config.SWDEBUG):
                    print("myURL=", myURL)
                req = requests.get(myURL,timeout=5)
                    
                returnJSON = req.json()

        except Exception:
                #traceback.print_exc()
                return {} 
        return returnJSON 

def sendNewNameToUnit(ipaddress, newName):

    myCommand = "setStationName?params=admin,"+newName
    sendCommandToWireless(ipaddress, myCommand)

def checkDeviceStatus(id):

    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")

    for single in wirelessJSON:
        ipAddress = single["ipaddress"]
        myID = single["id"]
        if (str(id).replace(" ","") == str(myID)):
            myJSON = checkForDeviceFromIP(ipAddress)
            if (len(myJSON) > 0):
                #pclogging.systemlog(config.INFO,"Wireless Device ID %s Active" %(myID))

                return True
            else:
                #pclogging.systemlog(config.INFO,"Wireless Device ID %s Inactive" %(myID))
                return False

    return False 
       
def isDeviceActive(id):
    try:
        if (state.deviceStatus[id] == True):
            return True
        else:
            return False
    except:
        return False

def findWirelessExtenders():
    IPAddr = subprocess.check_output(['hostname', '-I'])
       
    IPAddr = IPAddr.decode()
    IPAddr = IPAddr.split(" ")
    print("Your Computer IP Address is:" + IPAddr[0])  
    myNetIP = IPAddr[0].split(".")
    myNetIP = myNetIP[0]+"."+myNetIP[1]+"."+myNetIP[2]+".0"
    CIDR = ipaddress.IPv4Network(myNetIP+"/24")
    print("Your Computer CIDR is:", CIDR)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", str(now))
    returnJSON = []

    for ip in ipaddress.IPv4Network(CIDR):

    
        print ("checking IP:", str(ip))
        JSON = checkForDeviceFromIP(ip)
        if len(JSON) != 0:
            # check for SGS JSON
            #print("JSON[1]=", JSON[1])
            
            DumpedJSON = json.dumps(JSON[1])
            DumpedJSON = json.loads(DumpedJSON)
            DumpedJSON = json.loads(DumpedJSON)
            #print("DumpedJOSN =", DumpedJSON)
            try:
                if (len(DumpedJSON["id"]) == 4):
                    if (len(DumpedJSON["return_string"]) > 0):
                        print ("SGS Wireless Extender Found.  ID=", DumpedJSON["id"])
                        returnJSON.append(JSON)

            except:
                #traceback.print_exc()
                pass
            
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Finish Time =", str(now))
    print ("returnJSON", returnJSON)

    return returnJSON 

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

def checkForDeviceFromIP(ip):
        myMQTTIP = get_ip_address()
        myMQTTPort  = 1883
        myURL = 'http://'+str(ip)+'/checkForID?params='+myMQTTIP+','+str(myMQTTPort)
        
        completeResponse = subprocess.run(['ping','-c1', '-w 1 ',str(ip)],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
        #response = subprocess.run(['ping','-c1', '-W 1',str(ip)],stdout=None, stderr=None) 
        #print("completeResponse.returncode =", completeResponse.returncode)
        #print("ipaddress=",ip)
        returnJSON = {}
        if completeResponse.returncode == 0:
            try:
                req = requests.get(myURL,timeout=5)

               
                returnJSON = req.json()

            except Exception:
                #traceback.print_exc()
                return {} 
        return returnJSON





def updateDeviceStatus(Log):


    #state.deviceStatus = {} 
    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
    for single in wirelessJSON:
        myID = str(single["id"])
        if (checkDeviceStatus(single["id"])):
            try:
                if (state.deviceStatus[str(single['id'])] == False):
                     pclogging.systemlog(config.INFO,"Wireless Device ID %s Reactivated" %(myID))
            except:
                #traceback.print_exc()
                pass
            if (Log): 
                pclogging.systemlog(config.INFO,"Wireless Device ID %s Active" %(myID))
                
            state.deviceStatus[str(single["id"])] =   True
        else:
            try:
                if (state.deviceStatus[str(single['id'])] == True):
                    pclogging.systemlog(config.INFO,"Wireless Device ID %s has gone Inactive" %(myID))
            except:
                #traceback.print_exc()
                pass
            state.deviceStatus[str(single["id"])] =   False
            if (Log): 
                pclogging.systemlog(config.INFO,"Wireless Device ID %s is Inactive" %(myID))
            state.deviceStatus[str(single["id"])] =   False


def getNameForID(myID):


       

    for single in wirelessJSON:
        if (str(myID).replace(" ", "") == str(single["id"]).replace(" ", "")): 
            return (single["name"])
    
    return "Unknown Device"

    

