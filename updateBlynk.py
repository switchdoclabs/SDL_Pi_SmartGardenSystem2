from __future__ import print_function

# provides routine to update SGS Blynk Display
from builtins import str
from builtins import range
import time
import requests
import json
import util
import state
# Check for user imports
import config
import readJSON
import traceback
import psutil
import AccessValves
import MQTTFunctions
import pclogging


DEBUGBLYNK = False 



def blynkSetValvesOff(base):

    for i in range(1,9):
        virtualPin = "V"+ str(i+ base)
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+virtualPin+'?value=255')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+virtualPin+'?color=%23FF0000') # Red


def blynkSetValves(myID, base):
   myValveState = pclogging.getValveState(myID)
   for i in range(1,9):
        valve = myValveState[i]
        #print("valve[%i]=%s" % (i, valve))
        virtualPin = "V"+str(base+i)
        #print("vitualPin", virtualPin) 
        if (valve == "1"):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+virtualPin+'?color=%2300FF00') # Green
        else:
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+virtualPin+'?color=%23FF0000') # Red


def blynkInit():
    # initalize button states
    try:
        blynkSetValvesOff(29)
        blynkSetValvesOff(49)
        # selectors
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V45?value=0')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V49?value=0')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V46?value=0')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V22?value=')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V23?value=')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V24?value=')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V25?value=')
        
        # SecondsToTurnOn
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V47?value='+str(state.SecondsToTurnOn))
        # TurnOnValveButton
        #BlinkWirelessUnit
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V48?value=0')
        put_body = "?value=No Wireless Unit Selected"
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V39', data=put_body )
        time.sleep(0.5)
        put_body = "?value=No Wireless Unit Selected"
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V40', data=put_body)
        if (config.manual_water == False):
            # set the label to disabled 
            label = "Disabled"
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?offLabel='+label)
            if (DEBUGBLYNK):
                print("blynkInit:WaterDisabled:r.status_code:",r.status_code)
        else:
            label = "Turn On Valve"
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?offLabel='+label)
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?offBackColor=%230000FF') # Blue
            if (DEBUGBLYNK):
                print("blynkInit:WaterEnabled:r.status_code:",r.status_code)
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?value=0')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V5?color=%23FF0000') # Red

        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V5?value=255')

        
    except Exception as e:
        print("exception in blynkInit")
        print (e)
        return 0

def updateStaticBlynk():
        put_header={"Content-Type": "application/json"}

        val = str(len(readJSON.getJSONValue("WirelessDeviceJSON")))
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V13', data=put_body, headers=put_header)
        val = str(config.valve_count)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V14', data=put_body, headers=put_header)
        val = str(config.moisture_sensor_count)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V15', data=put_body, headers=put_header)


        # now do the choices on page two and three
        myJSONWireless = readJSON.getJSONValue("WirelessDeviceJSON")
        labels = ""
        for single in myJSONWireless:
            myName = str(single["id"])+"/"+single["name"]+"/"+single["ipaddress"]
            labels = labels + "'"+ myName +"',"
           
        '''
        put_body = "?labels="+"\""+labels+"\""
        put_body="?labels=\"Test1\",\"Test2\""
        print("put_body=", put_body)
        myRequest= config.BLYNK_URL+config.BLYNK_AUTH+'/update/V45'+put_body
        print("myRequest=", myRequest)
        r = requests.get(myRequest)

        #r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V45', data=put_body, headers=put_header)
        #r = requests.get(myRequest,headers=put_header)
        if (DEBUGBLYNK):
                print("updateStaticBlynk:V45 Labels:r.status_code:",r.status_code)
       ''' 
            
    
def blynkResetButton(buttonNumber):
    try:
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+buttonNumber+'?value=0')
    except Exception as e:
        print("exception in blynkResetButton")
        print (e)
        return 0

def blynkEventUpdate():
    try:
        put_header={"Content-Type": "application/json"}
        val = state.Last_Event 
        put_body = json.dumps([val])
        if (DEBUGBLYNK):
          print("blynkEventUpdate:",val)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V10', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkEventUpdate:POST:r.status_code:",r.status_code)
        return 1
    except Exception as e:
        print("exception in blynkEventUpdate")
        print (e)
        return 0


def blynkTerminalUpdate(entry):
    try:
        put_header={"Content-Type": "application/json"}

        entry = time.strftime("%Y-%m-%d %H:%M:%S")+": "+entry+"\n"
        put_body = json.dumps([entry])
        if (DEBUGBLYNK):
            print ("blynkTerminalUpdate:Pre:put_body:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V26', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print ("blynkTerminalUpdate:POST:r.status_code:",r.status_code)
    except Exception as e:
        print ("exception in blynkTerminalUpdate")
        print (e)
        return 0


def blynkStateUpdate():
    try:
        put_header={"Content-Type": "application/json"}

        if (DEBUGBLYNK):
            print("blynkStateUpdate:")
        blynkEventUpdate()

        # do our percentage active
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")

        active = 0 
        for single in wirelessJSON:
            if (state.deviceStatus[single['id']]  == True):
                active = active + 1
        myPercent = 100.0*active/len(state.deviceStatus) 
        # do the graphs
        val = "{:4.1f}".format(myPercent)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V1', data=put_body, headers=put_header)

        if (state.lastMainReading != "Never"):
            val = state.Hour24_AQI
            put_body = json.dumps([val])
            if (DEBUGBLYNK):
                print("blynkStateUpdate:Pre:put_body:",put_body)
            r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V11', data=put_body, headers=put_header)
            if (DEBUGBLYNK):
                print("blynkStateUpdate:POST:r.status_code:",r.status_code)
     
            val = util.returnTemperatureCF(state.OutdoorTemperature)
            put_body = json.dumps([val])
            r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V12', data=put_body, headers=put_header)
    
    
        # do the boxes
    
        val = "{:4.1f}%".format(psutil.cpu_percent() )
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V2', data=put_body, headers=put_header)
    
        val = "{:4.1f}%".format(psutil.virtual_memory().percent )
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V3', data=put_body, headers=put_header)

        myValue = psutil.disk_usage('/')
        myDPercent = myValue[3]
        myDPercent = 100.0 - myDPercent
   
        val = "{:4.1f}%".format(myDPercent)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V4', data=put_body, headers=put_header)
    
        # page 2 SensorsLevels
        myID = ""
        myName = "No Wireless Unit Selected"
        PlantIPAddress = ""
        if (state.WirelessDeviceSelectorPlant > 0):
            myJSONWireless = readJSON.getJSONValue("WirelessDeviceJSON")
            i = 0 
            if (len(myJSONWireless) > state.WirelessDeviceSelectorPlant):
                myName = str(i)+":"+"No Wireless Unit Selected"
                myID = ""
            for single in myJSONWireless:
                i = i+ 1
                if ( state.WirelessDeviceSelectorPlant  == i): 
                    myName = str(i)+": "+str(single["id"])+"/"+single["name"]+"/"+single["ipaddress"]
                    PlantIPAddress = single["ipaddress"]
                    myID = single["id"]
            if (myID != ""):
                print("setting Valves by Plant")
                blynkSetValves(myID, 29)
           
            # now have ID, so can find sensor values
            if (len(state.moistureSensorStates) > 0):
                for singleSensor in state.moistureSensorStates:
                    if (str(singleSensor["id"]) == str(myID)):
                        updateVirtual = "V"+str(int(singleSensor["sensorNumber"]) + 21)
                        val = "{:4.1f}%".format( float(singleSensor["sensorValue"]))
                        put_body = json.dumps([val])
                        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+updateVirtual, data=put_body, headers=put_header)


        
        if (state.WirelessDeviceSelectorControl > 0):
            myJSONWireless = readJSON.getJSONValue("WirelessDeviceJSON")
            if (len(myJSONWireless) > state.WirelessDeviceSelectorControl):
                myID = ""
                i = 0
                for single in myJSONWireless:
                    i = i+ 1
                    if ( state.WirelessDeviceSelectorControl  == i): 
                        myID = single["id"]
                if (myID != ""):
                    print("setting Valves by Control")
                    blynkSetValves(myID,49)

        return 1
    except Exception as e:
        print (traceback.format_exc())
        print("exception in blynkStateUpdate")
        print (e)
        return 0

def blynkStatusUpdate():

    if (DEBUGBLYNK):
        print("blynkStatusUpdate Entry")
    try:
        put_header={"Content-Type": "application/json"}

        # read button and menu selection states
        # state.WirelessDeviceSelectorPlant 
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V49') # read button state
        myText = r.text
        #print("myTextB=", myText)
        if (myText == "[]"):
            myText = "0"
        myText = myText.replace('["','')
        myText = myText.replace('"]','')
        #print("myText=", myText)
        state.WirelessDeviceSelectorPlant =  int(myText)
        # now do the choices on page two and three
        myName = "No Wireless Unit Selected"
        PlantIPAddress = ""
        if (state.WirelessDeviceSelectorPlant > 0):
            myJSONWireless = readJSON.getJSONValue("WirelessDeviceJSON")
            i = 0 
            if (len(myJSONWireless) > state.WirelessDeviceSelectorPlant):
                myName = str(i)+":"+"No Wireless Unit Selected"
            for single in myJSONWireless:
                i = i+ 1
                if ( state.WirelessDeviceSelectorPlant  == i): 
                    myName = str(i)+": "+str(single["id"])+"/"+single["name"]+"/"+single["ipaddress"]
                    PlantIPAddress = single["ipaddress"]
           
        val = myName 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V40', data=put_body, headers=put_header)

        # state.WirelessDeviceSelectorControl 
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V45') # read button state
        myText = r.text
        if (myText == "[]"):
            myText = "0"
        myText = myText.replace('["','')
        myText = myText.replace('"]','')
        state.WirelessDeviceSelectorControl =  int(myText)

        # now do the choices on page two and three
        myControlName = "No Wireless Unit Selected"
        ControlIPAddress = ""
        ControlID = ""
        if (state.WirelessDeviceSelectorControl > 0):
            myJSONWireless = readJSON.getJSONValue("WirelessDeviceJSON")
            i = 0 
            if (len(myJSONWireless) > state.WirelessDeviceSelectorControl):
                myControlName = str(i)+":"+"No Wireless Unit Selected"
            for single in myJSONWireless:
                i = i+ 1
                if ( state.WirelessDeviceSelectorControl  == i): 
                    myControlName = str(i)+": "+str(single["id"])+"/"+single["name"]+"/"+single["ipaddress"]
                    ControlIPAddress = single["ipaddress"]
                    ControlID = str(single["id"]) 
           
        val = myControlName 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V39', data=put_body, headers=put_header)

        # state.ValveSelector
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V46') # read button state
        myText = r.text
        if (myText == "[]"):
            myText = "0"
        myText = myText.replace('["','')
        myText = myText.replace('"]','')
        state.ValveSelector =  int(myText)

        # state.SecondsToTurnOn
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V47') # read button state
        myText = r.text
        if (myText == "[]"):
            myText = "0"
        myText = myText.replace('["','')
        myText = myText.replace('"]','')
        state.SecondsToTurnOn =  int(myText)

        # state.TurnOnValveButton
        # Look for Valve turn on 
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V41') # read button state
        
        if (r.text == '["1"]'):
            state.TurnOnValveButton = True
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.TurnOnValveButton set to True")
        else:
            state.TurnOnValveButton = False
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.TurnOnValveButton set to False")
        # state.BlinkWirelessUnit
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V48') # read button state
        
        if (r.text == '["1"]'):
            state.BlinkWirelessUnit = True
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.BlinkWirelessUnit set to True")
        else:
            state.BlinkWirelessUnit = False
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.BlinkWirelessUnit set to False")

        if (DEBUGBLYNK):
            print("state.WirelessDeviceSelectorPlant =", state.WirelessDeviceSelectorPlant )

            print("state.WirelessDeviceSelectorControl =", state.WirelessDeviceSelectorControl) 
            print("state.ValveSelector =", state.ValveSelector)
            print("state.SecondsToTurnOn =", state.SecondsToTurnOn) 
            print("state.TurnOnValveButton =", state.TurnOnValveButton)
            print("state.BlinkWirelessUnit =", state.BlinkWirelessUnit)


        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V5?color=%23FF0000') # Red

        time.sleep(1)
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V5?color=%2300FF00') # Green
        # now deal with the button pushes

        if (state.BlinkWirelessUnit == True):
            if (ControlIPAddress != ""):
                myCommand = "blinkPixelCommand?params=admin"
                result = AccessValves.sendCommandToWireless(ControlIPAddress, myCommand)
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V48?value=0')
        if (state.TurnOnValveButton == True):
            if (ControlID != ""):
                if (state.ValveSelector >0):
                    if (state.SecondsToTurnOn > 0):
                        if (config.manual_water == True):
                            MQTTFunctions.sendMQTTValve(ControlID, str(state.ValveSelector), 1, str(state.SecondsToTurnOn))
                            message = "Manual Valve Actuated:"+ myControlName
                            pclogging.systemlog(config.INFO,message)
                 
                            pclogging.valvelog(ControlID, str(state.ValveSelector),1, "Manual Event ", "", state.SecondsToTurnOn)
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?value=0')


        blynkStateUpdate()
        return 1
    except Exception as e:
        print("exception in blynkStatusUpdate")
        print (e)
        return 0

def blynkAlarmUpdate():
    try:
        put_header={"Content-Type": "application/json"}

        #
        # Three LEDs
        # Moisture Alarm
        # Water Low Alarm 
        # Temperature Alarm
        # All three Orange For Moisture Fault
    
        # set all three to Green first


        if (config.DEBUG):
            print("===========")
            print("Alarm State")
            print("===========")
            print("Is_Alarm_Temperature=", state.Is_Alarm_Temperature) 
            print("Is_Alarm_Moisture=", state.Is_Alarm_Moisture) 
            print("Is_Alarm_MoistureFault=", state.Is_Alarm_MoistureFault) 
            print("Is_Alarm_AirQuality=", state.Is_Alarm_AirQuality) 
            print("Is_Alarm_WaterEmpty=", state.Is_Alarm_WaterEmpty) 

        if (DEBUGBLYNK):
            print("blynkAlarmUpdate:")
        put_body = json.dumps([255])
    
    
    
    
        if (state.Is_Alarm_MoistureFault):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V17?color=%23FF0000') # Red
            if (DEBUGBLYNK):
                print("blynkAlarmUpdate:MSF:r.status_code:",r.status_code)
    

            # post which sensors are bad

            for i in range(0,config.plant_number):
                if (state.Moisture_Humidity_Array[i] <= state.Alarm_Moisture_Sensor_Fault):
                    if (config.DEBUG):
                            print("Event Print Plant #{:d}---->Moisture Sensor Fault".format(i+1))
                    state.Last_Event = "Plant {:d} Moisture Sensor Fault".format(i+1)
                    blynkEventUpdate()
                    time.sleep(1)
        

            if (DEBUGBLYNK):
                print("blynkAlarmUpdate:MSF:r.status_code:",r.status_code)
        else:
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V17?color=%2300FF00') # Green

        if (state.Is_Alarm_Moisture):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V7?color=%23FF0000') # red
            if (DEBUGBLYNK):
                print("blynkAlarmUpdate:OTHER:r.status_code:",r.status_code)
        else:
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V7?color=%2300FF00') # Green
    
     
        if (state.Is_Alarm_AirQuality):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V8?color=%23FF0000') # red
            if (DEBUGBLYNK):
                print("blynkAlarmUpdate:OTHER:r.status_code:",r.status_code)
        else:
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V8?color=%2300FF00') # Green
    
        if (state.Is_Alarm_Temperature):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V9?color=%23FF0000') # red
            if (DEBUGBLYNK):
                print("blynkAlarmUpdate:OTHER:r.status_code:",r.status_code)
        else:
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V9?color=%2300FF00') # Green

        if (state.Is_Alarm_WaterEmpty):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V16?color=%23FF0000') # red
            if (DEBUGBLYNK):
                print("blynkAlarmUpdate:OTHER:r.status_code:",r.status_code)
        else:
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V16?color=%2300FF00') # Green


    
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V7?value=255')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V8?value=255')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V9?value=255')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V16?value=255')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V17?value=255')
    
        if (DEBUGBLYNK):
            print("blynkAlarmUpdate:POSTUPDATE:r.status_code:",r.status_code)
        
        return 1
    except Exception as e:
        print("exception in blynkAlarmUpdate")
        print (e)
        return 0

        
def blynkSGSAppOnline():

    try:
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/isAppConnected')
        if (DEBUGBLYNK):
            print("blynkSGSAppOnline:POSTCHECK:r.text:",r.text)
        return r.text
    except Exception as e:
        print("exception in blynkApponline")
        print (e)
        return ""

   
