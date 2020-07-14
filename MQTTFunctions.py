# MQTT Functions


import paho.mqtt.client as mqttClient
import time
import state
import config
import json
import pclogging
import datetime


def on_WirelessMQTTClientconnect(client, userdata, flags, rc):

    if rc == 0:

        #print("WirelessMQTTClient Connected to broker")

        state.WirelessMQTTClientConnected = True                #Signal connection

    else:

        print("WirelessMQTTClient Connection failed")

##############
#MQTT Message Types
##############

MQTTTESTMESSAGE = 0
MQTTVALVECHANGE = 1
MQTTALARM = 2
MQTTDEBUG = 3
MQTTSENSORS = 4

#############
# MQTT Publish Message Type
#############
MQTTPUBVALVESET = 10


##############
#MQTT Data Receiving
##############


def on_WirelessMQTTClientmessage(client, userdata, message):
    print ("Wireless MQTT Message received: ",   message.payload)

    MQTTJSON = json.loads(message.payload.decode("utf-8"))

    if (str(MQTTJSON['messagetype']) == str(MQTTVALVECHANGE)):
        if (config.SWDEBUG):
            print("Valve Change Received")
        pclogging.writeMQTTValveChangeRecord(MQTTJSON)

    if (str(MQTTJSON['messagetype']) == str(MQTTALARM)):
        if (config.SWDEBUG):
            print("Alarm Message Received")
        pclogging.systemlog(config.CRITICAL,MQTTJSON['argument'])

    if (str(MQTTJSON['messagetype']) == str(MQTTDEBUG)):
        if (config.SWDEBUG):
            print("Debug Message Recieved")
        temp = str(MQTTJSON['id'])+", "+str(MQTTJSON['value'])
        pclogging.systemlog(config.DEBUG,temp)

    if (str(MQTTJSON['messagetype']) == str(MQTTSENSORS)):
        if (config.SWDEBUG):
            print("Sensor Message Recieved")
        processSensorMessage(MQTTJSON)





def processSensorMessage(MQTTJSON):
        if (config.SWDEBUG):
            print("-----------------")
            print("Processing MQTT Sensor Message")
    
        parseSensors = MQTTJSON["sensorValues"]
        parseSensorsArray = parseSensors.split(",")
        for i in range(0,4):
            for singleSensor in state.moistureSensorStates:
                
                if (singleSensor["id"] == str(MQTTJSON["id"])):
                    if (singleSensor["sensorNumber"] == str(i+1)):
                       singleSensor["sensorValue"] = str(parseSensorsArray[i])
                       currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       singleSensor["timestamp"] = currentTime
        

        if (config.SWDEBUG):
            print("-----------------")
            print("MoistureSensorStates")
            print(state.moistureSensorStates)

            print("-----------------")
        for singleSensor in state.moistureSensorStates:
                pclogging.sensorlog(singleSensor["id"], singleSensor["sensorNumber"], singleSensor["sensorValue"], singleSensor["sensorType"], singleSensor["timestamp"]) 



##############
#End of MQTT Data Receiving
##############



def on_WirelessMQTTClientlog(client, userdata, level, buf):
    if (config.SWDEBUG):
        print("MQTT: ",buf)
    pass

def startWirelessMQTTClient():

    state.WirelessMQTTClientConnected = False   #global variable for the state of the connection

    broker_address= "127.0.0.1"  #Broker address
    port = 1883                         #Broker port

    state.WirelessMQTTClient = mqttClient.Client("SGS2")               #create new instance
    #client.username_pw_set(user, password=password)    #set username and password
    state.WirelessMQTTClient.on_connect= on_WirelessMQTTClientconnect                      #attach function to callback
    state.WirelessMQTTClient.on_message= on_WirelessMQTTClientmessage                      #attach function to callback
    state.WirelessMQTTClient.on_log = on_WirelessMQTTClientlog
    
    state.WirelessMQTTClient.connect(broker_address, port=port)          #connect to broker
    
    state.WirelessMQTTClient.loop_start()        #start the loop

#############
# MQTT Publish
#############

def sendMQTTValve(myID, Valve, State, TimeOn):

    myMessage = {
                    "id" : str(myID),
                    "messagetype" : str(MQTTPUBVALVESET),
                    "timestamp" : datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'),
                    "valve" : Valve,
                    "state" : State,
                    "timeon" : TimeOn
                    


                }
    myMessageJSON = json.dumps(myMessage)
    state.WirelessMQTTClient.publish("SGS/"+str(myID)+"/Valves",myMessageJSON )

