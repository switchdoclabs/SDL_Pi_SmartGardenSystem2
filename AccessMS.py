import state
import AccessValves
import readJSON
import config
import time
import datetime
import json
import pclogging


gain = 6144  # +/- 6.144V
sps = 250  # 250 samples per second

def initMoistureSensors():

        state.moistureSensorStates =[] 
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        for singleWireless in wirelessJSON:
            
            for i in range(1,5):
                element = {}
                element["id"] = str(singleWireless["id"])
                element["sensorType"] = "C1"
                element["sensorNumber"] = str(i)
                element["sensorValue"] = "0.0"
                element["timestamp"] = datetime.datetime.now()
                state.moistureSensorStates.append(element) 
            
            
#            myIP = singleWireless["ipaddress"]
#            myCommand = "enableMoistureSensors?params=admin,1,1,1,1"
#            returnJSON = AccessValves.sendCommandToWireless(myIP, myCommand)



def readAllMoistureSensors():
        # force read from wireless systems

        if (config.LOCKDEBUG):
            print("UpdateStateLock Acquire Attempt - readAllMoistureSensors ")
        state.UpdateStateLock.acquire()
        if (config.LOCKDEBUG):
            print("UpdateStateLock Acquired - readAllMoistureSensors ")

        #wireless extender
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        for singleWireless in wirelessJSON:

            myIP = singleWireless["ipaddress"]
            myCommand = "enableMoistureSensors?params=admin,1,1,1,1"
            returnJSON = AccessValves.sendCommandToWireless(myIP, myCommand)
            #print("returnJSON=", returnJSON)            

            myCommand = "readMoistureSensors?params=admin"
            returnJSON = AccessValves.sendCommandToWireless(myIP, myCommand)
            #print("returnJSON=", returnJSON)            
            if (len(returnJSON) != 0):
                parseSensors = returnJSON["return_string"]
                parseSensorsArray = parseSensors.split(",")
                for i in range(0,4):
                    for singleSensor in state.moistureSensorStates:
                        
                        if (singleSensor["id"] == singleWireless["id"]):
                            if (singleSensor["sensorNumber"] == str(i+1)):
                               singleSensor["sensorValue"] = str(parseSensorsArray[i*2+1])
                               currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                               singleSensor["timestamp"] = currentTime
            #myCommand = "enableMoistureSensors?params=admin,0,0,0,0"
            #returnJSON = AccessValves.sendCommandToWireless(myIP, myCommand)
            
            pass

        if (config.SWDEBUG):
            print("-----------------")
            print("MoistureSensorStates")
            print(state.moistureSensorStates)

            print("-----------------")
        for singleSensor in state.moistureSensorStates:
                pclogging.sensorlog(singleSensor["id"], singleSensor["sensorNumber"], singleSensor["sensorValue"], singleSensor["sensorType"], singleSensor["timestamp"]) 


        if (config.LOCKDEBUG):
            print("UpdateStateLock Releasing - readAllMoistureSensors")
        state.UpdateStateLock.release()
        if (config.LOCKDEBUG):
            print("UpdateStateLock Released - readAllMoistureSensors")



def readMSSensor(adsdevice, gdedevice, channel):

	    
      gdedevice.writeGPIO(channel, 1)
      time.sleep(0.200)
      Moisture_Raw   = adsdevice.readRaw(channel, gain, sps)
      if (Moisture_Raw > 0x7FFF):
           Moisture_Raw = 0 # Zero out negative Values
      Moisture_Raw = Moisture_Raw / 64 # scale to 10 bits
      
      Moisture_RawV   = adsdevice.readADCSingleEnded(channel, gain, sps) # Scale to 10 bits
      if (config.SWDEBUG):
           print( "Channel #%d Moisture_RawV=%0.2f" % (channel,Moisture_RawV))
                
              
      Moisture_Humidity = 0.0


      Moisture_Humidity = scaleMoistureCapacitance1(Moisture_Raw, channel)


      if (config.SWDEBUG):
          print( "Channel #%d -%s- Moisture_Raw =%0.2f, %0.2f" % (channel,"Cap:" , Moisture_Raw, Moisture_Humidity ))
       		

      gdedevice.writeGPIO(channel, 0)
      #time.sleep(0.25)
      #gdedevice.writeGPIO(channel, 0)

                 		
      if (config.SWDEBUG):
            print( "Channel #%d Pre Limit Moisture_Humidity=%0.2f" % (channel, Moisture_Humidity))
      if (Moisture_Humidity >100): 
             Moisture_Humidity = 100;
      if (Moisture_Humidity <0): 
             Moisture_Humidity = 0;
                    
      if (config.SWDEBUG):
             print( "Channel #%d Moisture Humidity = %0.2f" % (channel, Moisture_Humidity))
      if (config.SWDEBUG):
              print("------------------------------")
      return Moisture_Humidity
                   



# scale for capacitance sensor 1
def scaleMoistureCapacitance1(Moisture_Raw, PlantNumber):
    # do the varying scale of the moisture for Capacitance readers 
    # do the varying scale of the moisture
    # based on 10 bit values
    # > #0 100%
    #  = #1 0%
    # scale to 0% from there
    #
    # first number is for 0%, second is 100%
    sensorCal = [363, 150]
    if (Moisture_Raw < sensorCal[1]):
          Moisture_Humidity = 100
    else:
          Moisture_Humidity = ((sensorCal[0] - Moisture_Raw)*100.0)/(sensorCal[0] - sensorCal[1])
                            

    if (Moisture_Humidity < 0):
        Moisture_Humidity = 0.0

    return round(Moisture_Humidity,2)

