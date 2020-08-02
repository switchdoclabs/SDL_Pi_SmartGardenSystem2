import time
import config
import state
import datetime
import AccessValves
import scanForResources
import pclogging




def valveCheck():
    if (config.SWDEBUG):
        print(">>>>>>Valve Check<<<<<<")


    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquire Attempt - valveCheck")
    state.UpdateStateLock.acquire()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquired - valveCheck")

    myValves = config.SGSConfigurationJSON["Valves"]
    for single in myValves:
        
      if(scanForResources.isDeviceActive(single["id"]) == True):

        ################# 
        # check for timed
        ################# 

        if (single["Control"] == "Timed"):
           
            if (stateValveCheck(single["id"],single["ValveNumber"])):
                    #print("valveState Found for",single["id"],single["ValveNumber"])
                    NextTime = stateValveFetchTime(single["id"],single["ValveNumber"])
                    nowTime = datetime.datetime.now()
                    
                    if (NextTime <= nowTime): 
                   
                        #set up next fire
                        timeDelta = getTimeDelta(single["TimerSelect"])
                        while NextTime < nowTime:
                            NextTime = NextTime + timeDelta
                        stateValveUpdateTime(single["id"],single["ValveNumber"],NextTime)
                        AccessValves.turnOnTimedValve(single)
                        if (config.SWDEBUG):
                             print("Timer Fired!  Next Fire=",NextTime)
                        pclogging.valvelog(single["id"], single["ValveNumber"], 1, "Timer Event ", "", single["OnTimeInSeconds"])

            else:
                
                myNextTime = calculateFirstTime(single)
                newValve = {
                    "id" : single["id"],
                    "ValveNumber" : single["ValveNumber"],
                    "NextTime": myNextTime,
                    "LengthTurnOn": single["OnTimeInSeconds"]
                    }
                state.valveStatus.append(newValve)
        
        ################# 
        # check for MS Control
        ################# 
       
        myControl = single["Control"]
        
        if (myControl[0:2] == "MS"):   # found Moisture sensor

            # check for 15 minute lapse
            # never do pump turn ons because of MS control more than
            # every 15 minutes
            
            if (state.nextMoistureSensorActivate < datetime.datetime.now()):
                if (config.SWDEBUG):
                    print ("READY TO CHECK FOR MS and PUMP")
                mySplit = myControl.split("/")

                MSNumber = mySplit[0][3:]
                Name = mySplit[1]
                myID = mySplit[2]
            

                myMoistureSensor = getMoistureReading(myID, MSNumber)
                myMoistureReading = myMoistureSensor["sensorValue"]
                myMoistureSensorType = myMoistureSensor["sensorType"]
           
                # check for threshold
                # less than 5% means bad sensor, do nothing
                if (float(myMoistureReading) > 5.0):

                    # check for over Moisture threshold
                    if (config.SWDEBUG):
                        print("current valve=",single)
                        print("current MS Reading=",myMoistureSensor)
                    myThreshold = float(single["MSThresholdPercent"])
                    if (myThreshold > float(myMoistureReading)):
                        if (config.SWDEBUG):
                            print("turn ON Valve #", single["id"], single["ValveNumber"])
                        AccessValves.turnOnTimedValve(single)
                        if (config.SWDEBUG):
                            print("Valve Turned On by MS Sensor#%s/%s/%s for %s Seconds " % (MSNumber, Name, myID, single["OnTimeInSeconds"]  ))
                        pclogging.valvelog(single["id"], single["ValveNumber"], 1, "MS Sensor "+str(myThreshold) + ">" + str(myMoistureReading), "", single["OnTimeInSeconds"])
                    else:
                        if (config.SWDEBUG):
                            print("NO Change on Valve #", single["id"], single["ValveNumber"])
                        pass

                else:
                    if (config.SWDEBUG):
                        print("Bad Sensor Found:", myMoistureSensor)
      else:
          if (config.SWDEBUG):
                        print("Inactive Wireless Device %s / Valve %s " %( str(single["id"]), str(single["ValveNumber"])))

    # update nextMoistureSensorActivate
    myNow = datetime.datetime.now()
    while (state.nextMoistureSensorActivate < myNow):
        state.nextMoistureSensorActivate = state.nextMoistureSensorActivate + datetime.timedelta( minutes=15)
        if (config.SWDEBUG):
            print("nextMoistureValveSensorCheck = ", state.nextMoistureSensorActivate)

    
    if (config.LOCKDEBUG):
        print("UpdateStateLock Releasing - valveCheck ")
    state.UpdateStateLock.release()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Released - valveCheck ")

def getMoistureReading(myID, myMSNumber):

    for singleSensor in state.moistureSensorStates:
        if (singleSensor["id"].replace(" ", "") == myID.replace(" ", "")):
            if (int(singleSensor["sensorNumber"]) == int(myMSNumber)):
                return singleSensor 


        



def getTimeDelta(timerValue):

    timeDelta = datetime.timedelta(minutes=15)

    if (timerValue == "Daily"):
        timeDelta = datetime.timedelta(days=1)
    if (timerValue == "12 Hours"):
        timeDelta = datetime.timedelta(hours=12)
    if (timerValue == "6 Hours"):
        timeDelta = datetime.timedelta(hours=6)
    if (timerValue == "3 Hours"):
        timeDelta = datetime.timedelta(hours=3)
    if (timerValue == "1 Hour"):
        timeDelta = datetime.timedelta(hours=1)
    if (timerValue == "30 Minutes"):
        timeDelta = datetime.timedelta(minutes=30)
    if (timerValue == "15 Minutes"):
        timeDelta = datetime.timedelta(minutes=15)
    return timeDelta 

def calculateFirstTime(single):
    
    nowTime = datetime.datetime.now() 
    myTempTime = single["StartTime"].split(":")
  
   
    timeDelta = getTimeDelta(single["TimerSelect"])

    
    
    
    myStartTime = nowTime.replace(hour=int(myTempTime[0]), minute=int(myTempTime[1]),second=0,microsecond=0)

    if (myStartTime > nowTime):
        NextTime = myStartTime 
    else:
        NextTime = myStartTime + timeDelta

   
    return NextTime
    pass

def stateValveCheck(myID, myValveNumber):
    
    for vState in state.valveStatus:
        if(str(vState["id"]).replace(" ","") == str(myID).replace(" ","")):
            if(str(vState["ValveNumber"]).replace(" ","") == str(myValveNumber).replace(" ","")):
                 return True 
        
    return False

def stateValveFetchTime(myID, myValveNumber):
    
    for vState in state.valveStatus:
        if(str(vState["id"]).replace(" ","") == str(myID).replace(" ","")):
            if(str(vState["ValveNumber"]).replace(" ","") == str(myValveNumber).replace(" ","")):
                 return vState["NextTime"] 
        
    return None

def stateValveUpdateTime(myID, myValveNumber,NextTime):

    for vState in state.valveStatus:
        if(str(vState["id"]).replace(" ","") == str(myID).replace(" ","")):
            if(str(vState["ValveNumber"]).replace(" ","") == str(myValveNumber).replace(" ","")):
                vState["NextTime"] = NextTime 


def manualCheck():
   
    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquire Attempt -  manualCheck ")
    state.UpdateStateLock.acquire()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquired -  manualCheck ")

    pass

    if (config.LOCKDEBUG):
        print("UpdateStateLock Releasing -  manualCheck ")
    state.UpdateStateLock.release()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Released -  manualCheck ")

