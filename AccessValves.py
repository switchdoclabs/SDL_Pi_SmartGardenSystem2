import requests
import readJSON
import state
import config
import MQTTFunctions
import time

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


def turnOnTimedValve(singleValve):


    if (len(str(singleValve["id"]).replace(" ", "")) > 1):
        # wireless ID
        
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        '''
        for singlewireless in wirelessJSON:
            if (str(singleValve["id"]).replace(" ","") == str(singlewireless["id"]).replace(" ","")):
                    myIP = singlewireless["ipaddress"]

        myCommand = "setSingleValve?params=admin,"+str(singleValve["ValveNumber"])+",1,"+str(singleValve["OnTimeInSeconds"])
        sendCommandToWireless(myIP, myCommand)
        '''
        MQTTFunctions.sendMQTTValve(str(singleValve["id"]), str(singleValve["ValveNumber"]), 1, str(singleValve["OnTimeInSeconds"]))
        #
        # DEBUG slow down by 1 second
        #
        time.sleep(1)

def turnOffAllValves():

        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        for singlewireless in wirelessJSON:
            #adminpassword, valve0state, valve0length, valve1state, valve1state, .......
            myIP = singlewireless["ipaddress"]

            myCommand = "setValves?params=admin,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
            result = sendCommandToWireless(myIP, myCommand)
            if (config.SWDEBUG):
                print("return=", result)

            

