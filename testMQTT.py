
# 
# test MQTT coming from wireless units
#

import paho.mqtt.client as mqttClient
import time


def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")

        global Connected                #Use global variable
        Connected = True                #Signal connection

    else:

        print("Connection failed")

def on_message(client, userdata, message):
    print ("Message received: ",   message.payload)

def on_log(client, userdata, level, buf):
    print("log: ",buf)


Connected = False   #global variable for the state of the connection

broker_address= "127.0.0.1"  #Broker address
port = 1883                         #Broker port
#user = "smartgardensystem"                    #Connection username
#password = "password"            #Connection password

client = mqttClient.Client("SGS")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
client.on_log = on_log

client.connect(broker_address, port=port)          #connect to broker

client.loop_start()        #start the loop


# now read and get the wireless IDs
#
# topics are:

# SGS/<wirelessid>  ex:  SGS/124d

# read JSON
import state
import readJSON
import config



readJSON.readJSON("")
wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")

# subscribe to IDs
if (len(wirelessJSON) == 0):
    print("No Wireless SGS uinits present - run SGSConfigure.py")
    exit()

# wait for connection



while Connected != True:    #Wait for connection
    time.sleep(0.1)


# subscribe to IDs

for single in wirelessJSON:
    topic = "SGS/" + single["id"]
    print("subscribing to ", topic)
    client.subscribe(topic)

    topic = "SGS/" + single["id"]+"/Valves"
    print("subscribing to ", topic)
    client.subscribe(topic)

try:
    while True:
        time.sleep(15)
        #client.publish("SGS/5051/Valves", "Test")
        payload = '{"id": "5051", "messagetype": "10", "timestamp": "2020-06-27 15:30:28", "valve": "1", "state": 1, "timeon": "10"}'
        client.publish("SGS/5051/Valves", payload)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()

