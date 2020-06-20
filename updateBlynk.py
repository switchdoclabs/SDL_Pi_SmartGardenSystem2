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


DEBUGBLYNK = False 

def blynkInit():
    # initalize button states
    try:
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V5?value=0')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?value=0')
        if (config.manual_water == False):
            # set the label to disabled 
            label = "Disabled"
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?offLabel='+label)
            if (DEBUGBLYNK):
                print("blynkInit:WaterDisabled:r.status_code:",r.status_code)
        else:
            label = "Water Plant"
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?offLabel='+label)
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?offBackColor=%230000FF') # Blue
            if (DEBUGBLYNK):
                print("blynkInit:WaterEnabled:r.status_code:",r.status_code)

        
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V30?value=1')
    except Exception as e:
        print("exception in blynkInit")
        print (e)
        return 0

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

        put_body = json.dumps([entry])
        if (DEBUGBLYNK):
            print("blynkStateUpdate:Pre:put_body:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V31', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkStateUpdate:POST:r.status_code:",r.status_code)
    except Exception as e:
        print("exception in blynkTerminalUpdate")
        print (e)
        return 0
    

def blynkStateUpdate():
    try:
        put_header={"Content-Type": "application/json"}

        if (DEBUGBLYNK):
            print("blynkStateUpdate:")
        blynkEventUpdate()

        # do the graphs


        val = state.AirQuality_Sensor_Value 
        put_body = json.dumps([val])
        if (DEBUGBLYNK):
            print("blynkStateUpdate:Pre:put_body:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V11', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkStateUpdate:POST:r.status_code:",r.status_code)
    
        val = util.returnTemperatureCF(state.Temperature)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V12', data=put_body, headers=put_header)

        val = state.Humidity 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V14', data=put_body, headers=put_header)

        val = state.Sunlight_Vis 
        put_body = json.dumps([val])
        if (DEBUGBLYNK):
            print("blynkStateUpdate:Pre:put_bodyS:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V15', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkStateUpdate:POSTS:r.status_code:",r.status_code)

        # do the boxes
    
        val = "{:4.1f} {}".format(util.returnTemperatureCF(state.Temperature),util.returnTemperatureCFUnit() )
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V2', data=put_body, headers=put_header)
    
        val = "{:4.1f}{}".format(state.Humidity,"%")
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V3', data=put_body, headers=put_header)
    
        val = "{:4.1f}".format(state.Sunlight_Vis)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V4', data=put_body, headers=put_header)
    
        #gauges
    
              
        val = "{:4.1f}".format(state.Moisture_Humidity_Array[state.blynkPlantNumberDisplay-1])
        myLabel = "%23{:d} Plant Moisture".format(state.blynkPlantNumberDisplay)
        if (DEBUGBLYNK):
            print("blynkStateUpdate:myLable:", myLabel)
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V0?label='+myLabel) 
        if (DEBUGBLYNK):
            print("blynkStateUpdate:POSTM:r.status_code:",r.status_code)
        put_body = json.dumps([val])
        if (DEBUGBLYNK):
            print("blynkStateUpdate:PreM:put_body:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V0', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkStateUpdate:POSTM:r.status_code:",r.status_code)

        state.blynkPlantNumberDisplay = state.blynkPlantNumberDisplay + 1
        if (state.blynkPlantNumberDisplay > config.plant_number):
            state.blynkPlantNumberDisplay = 1
    
    
    
        percentWater = state.Tank_Percentage_Full 
        if (percentWater < config.Tank_Pump_Level):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V1?color=%23FF0000') # Red
        else:
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V1?color=%23FF8000') # Orange
    
        val = "{:4.1f}".format(percentWater)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V1', data=put_body, headers=put_header)
        
        # page 2 Moisture Levels

        for i in range(0,config.plant_number):
            val = "#{:1d}: {:4.1f}%".format(i+1, state.Moisture_Humidity_Array[i])
            put_body = json.dumps([val])
            updateVirtual = "V"+str(i+21)
            r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+updateVirtual, data=put_body, headers=put_header)
            
            if (state.Moisture_Humidity_Array[i] <= state.Alarm_Moisture_Sensor_Fault):
                r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+updateVirtual+'?color=%23FF0000') # Red
            else:
                if (state.Moisture_Humidity_Array[i] >= state.Moisture_Threshold):
                    r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+updateVirtual+'?color=%2300FF00') # Green
                else:
                    r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+updateVirtual+'?color=%23FFFFFF') # White
    
        

            
        

        return 1
    except Exception as e:
        print("exception in blynkStateUpdate")
        print (e)
        return 0

def blynkStatusUpdate():

    if (DEBUGBLYNK):
        print("blynkStatusUpdate Entry")
    try:
        put_header={"Content-Type": "application/json"}

        val = state.SGS_Values[state.SGS_State]
        if (DEBUGBLYNK):
            print("blynkStatusUpdate:",val)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V6', data=put_body, headers=put_header)
    
        # look for rainbow button change
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V5') # read button state
        if (DEBUGBLYNK):
            print("blynkStatusUpdate:POSTBR:r.status_code:",r.status_code)
            print("blynkStatusUpdate:POSTBR:r.text:",r.text)
    
        if (r.text == '["1"]'):
            state.runRainbow = True
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.runRainbow set to True")
        else:
            state.runRainbow = False
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.runRainbow set to False")

        # look for Turning LED Display Off button change
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V30') # read button state
        if (DEBUGBLYNK):
            print("blynkStatusUpdate:POSTBR:r.status_code:",r.status_code)
            print("blynkStatusUpdate:POSTBR:r.text:",r.text)
   
        
        if (r.text == '["1"]'):
            state.runLEDs = True
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.runLEDs set to True")
        else:
            state.runLEDs = False
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.runLEDs set to False")



        # look for plant water request
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V41') # read button state
        if (DEBUGBLYNK):
            print("blynkStatusUpdate:POSTPWR:r.status_code:",r.status_code)
            print("blynkStatusUpdate:POSTPWR:r.text:",r.text)
        if (r.text == '["1"]'):
            if (config.manual_water == True):
                if (state.Plant_Water_Request == False):
                    # fetch the plant number
                    r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V40') # read button state
                    # strip headers
                    myString = r.text
                    myString = myString.replace('["', "")
                    myString = myString.replace('"]', "")
                    state.Plant_Number_Water_Request = int(myString)
                    if (DEBUGBLYNK):
                        print("blynkStatusUpdate:POSTBRC:myString: ", myString)
                        print("blynkStatusUpdate:POSTBRC:r.text: ", r.text)
                        print("state.Plant_Number_Water_Request: ", state.Plant_Number_Water_Request)
                    #set request to True
                    state.Plant_Water_Request = True
                    if (DEBUGBLYNK):
                        print("blynkStatusUpdate:POSTBRC:state.Plant_WaterRequest set to True")
                else:
                    r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?value=1')
                    if (DEBUGBLYNK):
                        print("blynkStatusUpdate:POSTBRC:Plant_WaterRequest already pending")
            else:
                r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41?value=0')
                state.Plant_Water_Request = False
                state.Plant_Number_Water_Request = -1
                if (DEBUGBLYNK):
                    print("blynkStatusUpdate:POSTBRC:state.Plant_WaterRequest set to False")

        else:
            state.Plant_Water_Request = False
            state.Plant_Number_Water_Request = -1
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.Plant_WaterRequest set to False")
                print("blynkStatusUpdate:POSTBRC:state.runRainbow set to False")

        


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

   
