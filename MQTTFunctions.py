# MQTT Functions


import paho.mqtt.client as mqttClient
import time
import state
import config
import json
import pclogging

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

##############
#MQTT Data Receiving
##############


def on_WirelessMQTTClientmessage(client, userdata, message):
    print ("Wireless MQTT Message received: ",   message.payload)

    MQTTJSON = json.loads(message.payload.decode("utf-8"))

    if (MQTTJSON['messagetype'] == str(MQTTVALVECHANGE)):
        print("Valve Change Received")
        pclogging.writeMQTTValveChangeRecord(MQTTJSON)

    if (MQTTJSON['messagetype'] == str(MQTTALARM)):
        print("Alarm Message Received")
        pclogging.systemlog(config.CRITICAL,MQTTJSON['argument'])

    if (MQTTJSON['messagetype'] == str(MQTTDEBUG)):
        print("Debug Message Recieved")
        pclogging.systemlog(config.DEBUG,MQTTJSON['argument'])


##############
#End of MQTT Data Receiving
##############



def on_WirelessMQTTClientlog(client, userdata, level, buf):
    #if (config.SWDEBUG):
    print("log: ",buf)
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

