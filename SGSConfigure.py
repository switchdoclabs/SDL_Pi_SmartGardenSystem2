import time
import random
import threading
import remi.gui as gui
import urllib.request
from urllib.request import urlopen
from threading import Timer

from remi.gui import *
from remi import start, App
import json
import scanForResources
import requests
import ipaddress
import subprocess
import datetime
import sys
#import readJSON


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

myURLOpener = AppURLopener()

class SuperImage(gui.Image):
    def __init__(self, file_path_name=None, **kwargs):
        super(SuperImage, self).__init__("./static/SGfulllogocolor.png", **kwargs)
        
        self.imagedata = None
        self.mimetype = None
        self.encoding = None
        self.load(file_path_name)

    def load(self, file_path_name):
        self.mimetype, self.encoding = mimetypes.guess_type(file_path_name)
        with open(file_path_name, 'rb') as f:

            self.imagedata = f.read()
        self.refresh()

    def refresh(self):
        i = int(time.time() * 1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self), i)

    def get_image_data(self, update_index):
        headers = {'Content-type': self.mimetype if self.mimetype else 'application/octet-stream'}
        return [self.imagedata, headers]

class SGSConfigure(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')
        super(SGSConfigure, self).__init__(*args, static_file_path={'my_resources':res_path})

    def idle(self):
        try:
            self.progress.set_value((self.count/256.0)*100)
        
        except:
            pass

    def display_counter(self):
       
       #print ("self.count=", self.count)
       #print ("self.stop_flag=", self.stop_flag)
       self.progress.set_value((self.count/256.0)*100)
        
       Timer(1, self.display_counter).start() 
    
    def setDefaults(self):
        self.SWDEBUG = False
        self.enable_MySQL_Logging = False
        self.English_Metric = False
        self.MySQL_Password = "password"
        self.mailUser = "yourusername"
        self.mailPassword = "yourmailpassword"
        self.notifyAddress = "you@example.com"
        self.fromAddress = "yourfromaddress@example.com"
        self.enableText = False
        self.textnotifyAddress = "yournumber@yourprovider"
        self.enablePixel = False
        self.pixelPin = 21
        self.SolarMAX_Present = False
        self.SolarMAX_Type = "LEAD"
        self.BMP280_Altitude_Meters = 626.0
        self.Sunlight_Gain = 0
        self.weather = False
        self.USEWEATHERSTEM = False
        self.INTERVAL_CAM_PICS__SECONDS = 60
        self.STATIONKEY = ""
        self.WeatherUnderground_Present = False
        self.WeatherUnderground_StationID = "KWXXXXX"
        self.WeatherUnderground_StationKey = "YYYYYY"
        self.USEBLYNK = False
        self.BLYNK_AUTH = ""
        self.AS3935_Lightning_Config = "[2,1,3,0,3,3]"
        self.Camera_Night_Enable =  False
        self.REST_Enable = False 
        self.MQTT_Enable = False 
        self.MQTT_Server_URL = "" 
        self.MQTT_Port_Number = 5900 
        self.MQTT_Send_Seconds = 500 
        self.UltrasonicLevel = 4
        self.Tank_Pump_Level = 15.0
        self.manual_water = True
        self.WirelessDeviceJSON = ""

       
       
        self.dataDefaults = {} 

        self.dataDefaults['SWDEBUG'] = self.SWDEBUG 
        self.dataDefaults['enable_MySQL_Logging'] = self.enable_MySQL_Logging 
        self.dataDefaults['English_Metric'] = self.English_Metric 
        self.dataDefaults['MySQL_Password'] = self.MySQL_Password 
        self.dataDefaults['mailUser'] = self.mailUser 
        self.dataDefaults['mailPassword'] = self.mailPassword 
        self.dataDefaults['notifyAddress'] = self.notifyAddress 
        self.dataDefaults['fromAddress'] = self.fromAddress 
        self.dataDefaults['enableText'] = self.enableText 
        self.dataDefaults['textnotifyAddress'] = self.textnotifyAddress 
        self.dataDefaults['enablePixel'] = self.enablePixel 
        self.dataDefaults['pixelPin'] = self.pixelPin 
        self.dataDefaults['SolarMAX_Present'] = self.SolarMAX_Present 
        self.dataDefaults['SolarMAX_Type'] = self.SolarMAX_Type 
        self.dataDefaults['BMP280_Altitude_Meters'] = self.BMP280_Altitude_Meters 
        self.dataDefaults['Sunlight_Gain'] = self.Sunlight_Gain 
        self.dataDefaults['weather'] = self.weather 
        self.dataDefaults['USEWEATHERSTEM'] = self.USEWEATHERSTEM 
        self.dataDefaults['INTERVAL_CAM_PICS__SECONDS'] = self.INTERVAL_CAM_PICS__SECONDS 
        self.dataDefaults['STATIONKEY'] = self.STATIONKEY 
        self.dataDefaults['WeatherUnderground_Present'] = self.WeatherUnderground_Present 
        self.dataDefaults['WeatherUnderground_StationID'] = self.WeatherUnderground_StationID 
        self.dataDefaults['WeatherUnderground_StationKey'] = self.WeatherUnderground_StationKey 
        self.dataDefaults['USEBLYNK'] = self.USEBLYNK 
        self.dataDefaults['BLYNK_AUTH'] = self.BLYNK_AUTH 
        self.dataDefaults['AS3935_Lightning_Config'] = self.AS3935_Lightning_Config 
        self.dataDefaults['REST_Enable'] = self.REST_Enable 
        self.dataDefaults['MQTT_Enable'] = self.MQTT_Enable 
        self.dataDefaults['MQTT_Server_URL'] = self.MQTT_Server_URL 
        self.dataDefaults['MQTT_Port_Number'] = self.MQTT_Port_Number 
        self.dataDefaults['MQTT_Send_Seconds'] = self.MQTT_Send_Seconds 
        self.dataDefaults['UltrasonicLevel'] = self.UltrasonicLevel
        self.dataDefaults['Tank_Pump_Level'] = self.Tank_Pump_Level 
        self.dataDefaults['manual_water'] = self.manual_water 
        self.dataDefaults['WirelessDeviceJSON'] = self.WirelessDeviceJSON 
        

    def getJSONValue(self, entry):
        try:
            returnData = self.JSONData[entry]
            return returnData
        except:
            print("JSON value not found - Set to Defaults:", entry)
            return self.dataDefaults[entry]



    def readJSONSGSConfiguration(self):
        if os.path.isfile('SGSConfiguration.JSON'):
            print ("SGSConfiguration.JSON File exists")
            with open('SGSConfiguration.JSON') as json_file:
                JSONData = json.load(json_file)
                #print("JSONData from SGSConfigFile=", JSONData)
                self.SGSConfigurationJSON  = JSONData 
        else:
            print ("SGSConfiguration.JSON File does not exist")
            self.SGSConfigurationJSON = {"SGSConfigVersion": "001",
                                        "Valves":  [] 
                                        }
            #print("Default JSONData for SGSConfigFile=", self.SGSConfigurationJSON)
            #self.setDefaults()

        
    def readJSON(self):

        self.setDefaults()

        if os.path.isfile('SGS.JSON'):
            print ("SGS.JSON File exists")
            with open('SGS.JSON') as json_file:
                self.JSONData = json.load(json_file)


                #print("JSONData from File=", self.JSONData)
                self.SWDEBUG = self.getJSONValue('SWDEBUG')
                self.enable_MySQL_Logging = self.getJSONValue('enable_MySQL_Logging')
                #print("enable_mySQL_Logging=", self.enable_MySQL_Logging)
                self.English_Metric = self.getJSONValue('English_Metric')
                self.MySQL_Password = self.getJSONValue('MySQL_Password')
                self.mailUser = self.getJSONValue('mailUser')
                self.mailPassword = self.getJSONValue('mailPassword')
                self.notifyAddress = self.getJSONValue('notifyAddress')
                self.fromAddress = self.getJSONValue('fromAddress')
                self.enableText = self.getJSONValue('enableText')
                self.textnotifyAddress = self.getJSONValue('textnotifyAddress')
                self.enablePixel = self.getJSONValue('enablePixel')
                self.pixelPin = self.getJSONValue('pixelPin')
                self.SolarMAX_Present = self.getJSONValue('SolarMAX_Present')
                self.SolarMAX_Type = self.getJSONValue('SolarMAX_Type')
                self.BMP280_Altitude_Meters = self.getJSONValue('BMP280_Altitude_Meters')
                self.Sunlight_Gain = self.getJSONValue('Sunlight_Gain')
                self.weather = self.getJSONValue('weather')
                self.USEWEATHERSTEM = self.getJSONValue('USEWEATHERSTEM')
                self.INTERVAL_CAM_PICS__SECONDS = self.getJSONValue('INTERVAL_CAM_PICS__SECONDS')
                self.STATIONKEY = self.getJSONValue('STATIONKEY')
                self.WeatherUnderground_Present = self.getJSONValue('WeatherUnderground_Present')
                self.WeatherUnderground_StationID = self.getJSONValue('WeatherUnderground_StationID')
                self.WeatherUnderground_StationKey = self.getJSONValue('WeatherUnderground_StationKey')
                self.USEBLYNK = self.getJSONValue('USEBLYNK')
                self.BLYNK_AUTH = self.getJSONValue('BLYNK_AUTH')
                self.AS3935_Lightning_Config = self.getJSONValue('AS3935_Lightning_Config')
                self.Camera_Night_Enable = self.getJSONValue('Camera_Night_Enable')
                self.REST_Enable = self.getJSONValue('REST_Enable')
                self.MQTT_Enable = self.getJSONValue('MQTT_Enable')
                self.MQTT_Server_URL = self.getJSONValue('MQTT_Server_URL')
                self.MQTT_Port_Number = self.getJSONValue('MQTT_Port_Number')
                self.MQTT_Send_Seconds = self.getJSONValue('MQTT_Send_Seconds')
                self.UltrasonicLevel = self.getJSONValue('UltrasonicLevel') 
                self.Tank_Pump_Level = self.getJSONValue('Tank_Pump_Level') 
                self.WirelessDeviceJSON = self.getJSONValue('WirelessDeviceJSON') 
        else:
            print ("SGS.JSON File does not exist")
            self.setDefaults()


    def saveSGSConfigurationJSON(self):

        data = self.SGSConfigurationJSON
        #print(data)

        #json_data = json.dumps(data)        
        
        
        with open('SGSConfiguration.JSON', 'w') as outfile:
            json.dump(data, outfile)

    def saveJSON(self):


        data = {}
        data['key'] = 'value'
        
        data['ProgramName'] = 'SmartGardenSystem2' 
        data['ConfigVersion'] = '001'        

        data['SWDEBUG'] = self.F_SWDEBUG.get_value()

        data['enable_MySQL_Logging'] = self.F_enable_MySQL_Logging.get_value()
        data['English_Metric'] = self.F_English_Metric.get_value()
        data['MySQL_Password'] = self.F_MySQL_Password.get_value()

        data['mailUser'] = self.F_mailUser.get_value()
        data['mailPassword'] = self.F_mailPassword.get_value()
        data['notifyAddress'] = self.F_notifyAddress.get_value()
        data['fromAddress'] = self.F_fromAddress.get_value()

        data['enableText'] = self.F_enableText.get_value()
        data['textnotifyAddress'] = self.F_textnotifyAddress.get_value()
        data['enablePixel'] = self.F_enablePixel.get_value()
        data['pixelPin'] = self.F_pixelPin.get_value()
        data['SolarMAX_Present'] = self.F_SolarMAX_Present.get_value()
        data['SolarMAX_Type'] = self.F_SolarMAX_Type.get_value()
        data['BMP280_Altitude_Meters'] = self.F_BMP280_Altitude_Meters.get_value()
        data['Sunlight_Gain'] = self.F_Sunlight_Gain.get_value()
        data['weather'] = self.F_weather.get_value()
        data['USEWEATHERSTEM'] = self.F_USEWEATHERSTEM.get_value()
        data['INTERVAL_CAM_PICS__SECONDS'] = self.F_INTERVAL_CAM_PICS__SECONDS.get_value()
        data['STATIONKEY'] = self.F_STATIONKEY.get_value()
        data['WeatherUnderground_Present'] = self.F_WeatherUnderground_Present.get_value()
        data['WeatherUnderground_StationID'] = self.F_WeatherUnderground_StationID.get_value()
        data['WeatherUnderground_StationKey'] = self.F_WeatherUnderground_StationKey.get_value()
        data['USEBLYNK'] = self.F_USEBLYNK.get_value()
        data['BLYNK_AUTH'] = self.F_BLYNK_AUTH.get_value()
        data['AS3935_Lightning_Config'] = self.F_AS3935_Lightning_Config.get_value()
        data['REST_Enable'] = self.F_REST_Enable.get_value()
        data['Camera_Night_Enable'] = self.F_Camera_Night_Enable.get_value()
        data['MQTT_Enable'] = self.F_MQTT_Enable.get_value()
        data['MQTT_Server_URL'] = self.F_MQTT_Server_URL.get_value()
        data['MQTT_Port_Number'] = self.F_MQTT_Port_Number.get_value()
        data['MQTT_Send_Seconds'] = self.F_MQTT_Send_Seconds.get_value()

        data['manual_water'] = self.F_manual_water.get_value()
        data['Tank_Pump_Level'] = self.F_Tank_Pump_Level.get_value()

        data['WirelessDeviceJSON'] = self.WirelessDeviceJSON


        # pins
        data['UltrasonicLevel'] = self.F_UltrasonicLevel.get_value()
        data['pixelPin'] = self.F_pixelPin.get_value()


        #print(data)

        json_data = json.dumps(data)        
        # strip double or triple \\
        
        with open('SGS.JSON', 'w') as outfile:
            json.dump(data, outfile)

    # screen builds

    def establishMenu(self,vbox):
        menu = gui.Menu(width='100%', height='30px')
        m0 = gui.MenuItem('SGS Configure', width=90, height=30)
        m0.onclick.do(self.menu_screen0_clicked)
        m05 = gui.MenuItem('Valve Report', width=90, height=30)
        m05.onclick.do(self.menu_screen05_clicked)
        m06 = gui.MenuItem('Name Change', width=90, height=30)
        m06.onclick.do(self.menu_screen06_clicked)
        m1 = gui.MenuItem('DM', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-TB', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('CMQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)

        menu.append([m0, m05, m06, m1, m2, m3, m4, m5, m6, m7])
    
    
        self.menubar = gui.MenuBar(width='100%', height='30px')
        self.menubar.append(menu)
        vbox.append(self.menubar)
        return vbox

    def buildScreen0(self):
        #screen 0

        # toplevel box
        vbox = gui.Container(width=1000, height=510, layout_orientation=gui.Container.LAYOUT_HORIZONTAL,  style="background: LightBlue")
        vbox.style['justify-content'] = 'center'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'

        # Menu
        menubox =  gui.Container(width=1000, height=30, style="background: LightGray")
        menubox = self.establishMenu(menubox)
        vbox.append(menubox)

        # Top Status block

        statusbox = gui.Container(width=1000, height=50, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style="background: LightBlue")
        #statusbox.style['justify-content'] = 'right'
        statusbox.style['align-items'] = 'right'
        statusbox.style['border'] = '2px'
        statusbox.style['border-color'] = 'blue'
        statusbox.style['flex-direction'] = 'row'

        # elements

        self.Display_IP = gui.Label('',width=130, height=30, margin='5px')

        self.Display_WEXT = gui.Label('', width=130, height=30, margin='5px')
        self.Display_EXT = gui.Label('', width=130, height=30, margin='5px')

        self.Display_WEXT.set_text('Found Wireless Extenders: ' )
        self.Display_IP.set_text('Scanning IP: N/A ' )


        #print("WirelessDeviceJSON=", self.WirelessDeviceJSON)
        #print("Length WirelessDeviceJSON=", len(self.WirelessDeviceJSON))
        if (len(self.WirelessDeviceJSON) == 0):

            scanForHardware = gui.Button('Scan For SGS Hardware',style='height: 30px; width:200px;  margin: 10px;  top:5px')
            scanForHardware.onclick.do(self.ScanForHardware)
            statusbox.append(scanForHardware,'scanForHardware') 


        else:
            RescanForHardware = gui.Button('ReScan For SGS Hardware',style=' height: 30px; width:200px;  margin: 10px;  top:5px')
            RescanForHardware.onclick.do(self.ScanForHardware)
            statusbox.append(RescanForHardware,'RescanForHardware') 
       


        statusbox.append(self.progress, 'progress')
        statusbox.append(self.Display_IP, 'DIP')
        statusbox.append(self.Display_WEXT, 'DWEXT')
        statusbox.append(self.Display_EXT, 'DEXT')

        vbox.append(statusbox)


    
        self.Display_WEXT.set_text('Found Wireless Extenders: '+ str(len(self.WirelessDeviceJSON) ))


        # Now set up the rows for configuation

        # set up valve configuration
        valves = []

    
        # wireless units 
        for wireless in self.WirelessDeviceJSON:
            wirelessDevice = wireless 
            #wirelessDevice = json.loads(str(wireless).replace("'", "\""))
            
            id = wirelessDevice['id'] 
            ipAddress = wirelessDevice['ipaddress']
            name = wirelessDevice['name']
            valves.append([id, name, ipAddress ])
            self.buildMissingValves(wirelessDevice['id'], wirelessDevice['name'])

            #vbox.append(wirelessBlock)
             

        
        items = ()
        self.ValveControlItems = ("Off","Timed")

        for ext in valves:
            if (len(str(ext[0])) < 4):
                    item = (str(ext[1])+" / "+str(ext[0]) +" / "+str(ext[2]))

            else:
                    item = (str(ext[1])+" / "+str(ext[0])+ " / " +str(ext[2]))
            
            for i in range(1,5):
                vcitem= ("MS#" + str(i)+ "/" + str(ext[1]) +"/"+ str(ext[0]))
                self.ValveControlItems = self.ValveControlItems + (vcitem, )
            items = items +  (item, )

        self.TimedItems = ("15 Minutes", "30 Minutes" , "1 Hour", "3 Hours", "6 Hours", "12 Hours", "Daily")


        # now set up new block
        self.ValveBlock = gui.Container(width=1000, height=500, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        self.ValveBlock.style['background'] = "LightGray"

        self.ValveBlock.style['align-items'] = 'right'
        self.ValveBlock.style['border'] = '2px'
        self.ValveBlock.style['border-color'] = 'blue'
        self.ValveBlock.style['flex-direction'] = 'row'




        self.listView1 = gui.ListView.new_from_list(items, width=400, height=25*len(valves), margin='10px')
        self.listView1.onselection.do(self.list_view_on_selected)
        self.ValveBlock.append(self.listView1)

        vbox.append(self.ValveBlock)
        

        return vbox

    def list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        print("selected_item_key=", selected_item_key)
        myUnit =  self.listView1.children[selected_item_key].get_text()
        # for on save
        self.current_listView_key = myUnit

        id = myUnit.split("/")[1]
        name = myUnit.split("/")[0]
        
        self.myValve = self.buildAValve(id, name,myUnit)
        self.ValveBlock.append(self.myValve, "currentValve") 


######################
# JSON Valve Functions
######################

    def checkValveJSON(self, myID, valveNumber):
        myJSON=self.SGSConfigurationJSON
        #print("myJSON=", self.SGSConfigurationJSON) 
        #myLoadedJSON = json.loads(str(myJSON).replace("'","\"" ))
        myLoadedJSON = myJSON
        #print("myValves=",myLoadedJSON["Valves"])
        myValves = myLoadedJSON["Valves"]

        Present = False
        for singleValve in myValves:

            if (str(singleValve["id"]).replace(" ","") == str(myID).replace(" ", "")):
                if (str(singleValve["ValveNumber"]) == str(valveNumber)):
                    Present = True
                    break

        return Present
    
    def addNewValveJSON(self, myID, valveNumber):

        # setup new Valve
        newValve = {
                "id": myID,
                "ValveNumber": valveNumber,
                "Control": "Off",
                "MSThresholdPercent": "65",
                "TimerSelect": "Daily",
                "StartTime": "05:00",
                "OnTimeInSeconds": "10",
                "ShowGraph" : False
                }
                

        myJSON=self.SGSConfigurationJSON
       
        
        myLoadedJSON = myJSON
        print(type(myLoadedJSON))
        #myLoadedJSON = myLoadedJSON.replace("'", "\"") 
        
        #myLoadedJSON = json.loads(myLoadedJSON)
        #print(type(myLoadedJSON))
        #print("myLoadedJSON A", myLoadedJSON)
        #myLoadedJSON = json.loads(str(myJSON).replace("'","\"" ))
        myLoadedJSON["Valves"].append(newValve)
        self.SGSConfigurationJSON = myLoadedJSON
        #self.SGSConfigurationJSON = json.dumps(myLoadedJSON)
    
         
        
    def fetchValveJSON(self, myID, valveNumber):
       
        myJSON=self.SGSConfigurationJSON
        
        #myLoadedJSON = json.loads(str(myJSON))
        #myLoadedJSON = json.loads(str(myJSON).replace("'","\"" ))
        myValves = myJSON["Valves"]

        for singleValve in myValves:
            #singleValve = json.loads(str(singleValve).replace("'","\"" ))
            #singleValve = json.loads(str(singleValve))
            if (str(singleValve["id"]).replace(" ", "") == str(myID).replace(" ", "")):
                if (str(singleValve["ValveNumber"]) == str(valveNumber)):
                    return singleValve
        return {}
        

    def updateValveJSON(self, myID, valveNumber):
        # update the JSON and return the list of Valves
        
        myValves = self.SGSConfigurationJSON["Valves"]

        for singleValve in myValves:
            #singleValve = json.loads(str(singleValve).replace("'","\"" ))
            #singleValve = json.loads(str(singleValve))
            
            #print("singleValve=", singleValve)
            #print("id=", singleValve["id"])
            #print("myID=", myID)
            #print("ValveNumber=", singleValve["ValveNumber"])
            #print("valveNumber=", valveNumber)
            if (str(singleValve["id"]).replace(" ", "") == str(myID).replace(" ", "")):
                if (str(singleValve["ValveNumber"]) == str(valveNumber)):
                    # OK, we have the correct one, so fix it
                    print("Valve Found for update")
                    print ("Before: updatedSingleValve=", singleValve)
                    singleValve["Control"] =  self.dropDownMSSensor.get_value()
                    singleValve["MSThresholdPercent"] = self.DisplayST_MS.get_text()
                    singleValve["TimerSelect"] = self.dropDownTimed.get_value()
                    singleValve["StartTime"] = self.DisplayST_TB.get_text()
                    print("Before-OTS", singleValve["OnTimeInSeconds"])
                    singleValve["OnTimeInSeconds"] = self.DisplayOTS_TB.get_text()
                    singleValve["ShowGraph"] = self.DisplaySG_CB.get_value() 

            
                    print("aftersingleValve-OTS", singleValve["OnTimeInSeconds"])
                    print ("updatedSingleValve=", singleValve)
                    #singleValve = json.dumps(singleValve)
             #myNewValves.append(singleValve)


        print("myValves=", myValves)
        
        self.SGSConfigurationJSON["Valves"] = myValves

        print ("updatedSGSConfigurationJSON=", self.SGSConfigurationJSON)

            
        pass
    
######################
# End JSON Valve Functions
######################

        
    def buildMissingValves(self, DeviceID, name ):
        #print("DeviceID=", DeviceID)
        #print("name=", name)
        
        if (len(str(DeviceID).replace(" ","")) < 4):
            for i in range(1,5):
                 if (self.checkValveJSON(DeviceID, i) == False):
                         # add a new one in
                         self.addNewValveJSON(DeviceID, i)
        else:
            for i in range(1,9):
                 if (self.checkValveJSON(DeviceID, i) == False):
                         # add a new one in
                         self.addNewValveJSON(DeviceID, i)

        pass



    def buildAValve(self, DeviceID, name, myUnit):
        myValve = gui.Container(width=300, height=400, layout_orientation=gui.Container.LAYOUT_VERTICAL)
        myValve.style['background'] = "LightBlue"

        myValve.style['align-items'] = 'right'
        myValve.style['border'] = '2px'
        myValve.style['border-color'] = 'blue'
        myValve.style['flex-direction'] = 'row'

        self.valvelist = ('None Selected',) 
        ext = myUnit.split("/")

        print ("myUnit---->=",myUnit)
        self.ValveJSON = {}

        if (len(str(ext[1])) < 4):
            for i in range(1,5):
                 self.valvelist = self.valvelist + (str(ext[0]) + "/" +str(ext[1]) + "/Valve "+str(i),)
                 # check to see if Valve is in JSON, add if not
                 myID = str(ext[1])
                 if (self.checkValveJSON(myID, i) == False):
                         # add a new one in
                         self.addNewValveJSON(myID, i)
                                          

        else:
            for i in range(1,9):
                 self.valvelist = self.valvelist + (str(ext[0]) + "/" +str(ext[1]) + "/Valve "+str(i),)
                 # check to see if Valve is in JSON, add if not
                 myID = str(ext[1])
                 if (self.checkValveJSON(myID, i) == False):
                         # add a new one in
                         self.addNewValveJSON(myID, i)
                                          



        self.DisplaySelect = gui.Label('Valve Select',width=100, height=15, margin='5px')
        self.dropDownValve = gui.DropDown.new_from_list(self.valvelist, width=200, height=20, margin='10px')
        
        self.dropDownValve.onchange.do(self.drop_down_valve_changed)
        self.dropDownValve.select_by_value('None' )        
        self.DisplayControl = gui.Label('Valve Control',width=100, height=15, margin='5px')

        self.dropDownMSSensor = gui.DropDown.new_from_list(self.ValveControlItems, width=200, height=20, margin='10px')

        self.dropDownMSSensor.select_by_value('Off' )        
        self.dropDownMSSensor.onchange.do(self.drop_down_MS_changed)

        self.DisplayMS = gui.Label('Moisture Sensor Threshold Percent',width=300, height=15, margin='10px')
        self.DisplayST_MS = gui.TextInput(width=100, height=15, style="margin:10px")

        self.DisplayTimed = gui.Label('Timer Selection',width=200, height=15, margin='10px')
        self.dropDownTimed = gui.DropDown.new_from_list(self.TimedItems, width=200, height=20, margin='10px')

        self.dropDownTimed.select_by_value('N/A' )        
        self.dropDownTimed.set_enabled(False)


        self.DisplayST = gui.Label('Start Time',width=200, height=15, margin='10px')

        self.DisplayST_TB = gui.TextInput(width=100, height=15, style="margin:10px")
        self.DisplayST_TB.set_enabled(False)

        self.DisplayOTS = gui.Label('On Time Length in Seconds',width=200, height=15, margin='10px')

        self.DisplayOTS_TB = gui.TextInput(width=100, height=15, style="margin:10px")
        self.DisplaySG_CB = gui.CheckBoxLabel( 'Display Graph', False, height=30, style='margin:5px; background: LightGray ')
       
        self.ValveSaveButton = gui.Button('Save Valve',height=30, width=100, margin=10)
        self.ValveSaveButton.onclick.do(self.onValveSaveButton)

        
        myValve.append(self.DisplaySelect)
        myValve.append(self.dropDownValve)
        myValve.append(self.DisplayControl)
        myValve.append(self.dropDownMSSensor)
        myValve.append(self.DisplayMS)
        myValve.append(self.DisplayST_MS)
        myValve.append(self.DisplayTimed)
        myValve.append(self.dropDownTimed)
        myValve.append(self.DisplayST)
        myValve.append(self.DisplayST_TB)
        myValve.append(self.DisplayOTS)
        myValve.append(self.DisplayOTS_TB)
        myValve.append(self.DisplaySG_CB)
        myValve.append(self.ValveSaveButton)


        return myValve 

    def onValveSaveButton (self, widget, name='', surname=''):
        print("onValveSaveButton Clicked")
        myUnit = self.current_listView_key 
        
        myID = myUnit.split("/")[1]
        name = myUnit.split("/")[0]
        
        self.updateValveJSON(myID, self.currentValveNumber)

    def drop_down_MS_changed (self, widget, selected_item_key):
        myUnit = selected_item_key
        print ("myUnit=", myUnit)
        if (myUnit == 'Timed'):
            print('enabled')
            self.DisplayST_TB.set_enabled(True)
            self.dropDownTimed.set_enabled(True)
        else:
            print('disabled')
            self.DisplayST_TB.set_enabled(False)
            self.dropDownTimed.set_enabled(False)


    def drop_down_valve_changed (self, widget, selected_item_key):
        myUnit = selected_item_key
        # parse values
        splitMyUnit = myUnit.split("/")
        # get the default values
        #print ('valveJSON=', valveJSON)
        if (myUnit != "None Selected"):
            values = myUnit.split("/")
            vnum = values[2].split(" ")
            self.currentValveNumber = vnum[1]
            valveJSON = self.fetchValveJSON(values[1], self.currentValveNumber)

            print (type(valveJSON))
            print ("myValveJSON=", valveJSON)
            # now set up the other menu items
            #valveJSON = json.loads(str(valveJSON))
            #valveJSON = json.loads(str(valveJSON).replace("'","\"" ))

            self.dropDownMSSensor.select_by_value(valveJSON["Control"] )        
            self.dropDownTimed.select_by_value(valveJSON["TimerSelect"])
            self.DisplayST_MS.set_text(valveJSON["MSThresholdPercent"])
            self.DisplayST_TB.set_text(valveJSON["StartTime"])
            self.DisplayOTS_TB.set_text(valveJSON["OnTimeInSeconds"])
            self.DisplaySG_CB.set_value(valveJSON["ShowGraph"])
            if (valveJSON["Control"]  == 'Timed'):
                print('enabled')
                self.DisplayST_TB.set_enabled(True)
                self.dropDownTimed.set_enabled(True)
            else:
                print('disabled')
                self.DisplayST_TB.set_enabled(False)
                self.dropDownTimed.set_enabled(False)
       


        else:
            print ("None Selected")
                
        

    

    def buildScreen05(self):


        #screen 05

        vbox = VBox(width=1000, height=510, style="background: LightGray")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        #screen 05

        vbox = self.establishMenu(vbox)



        screen1header = gui.Label("Valve Configuration Report", style='margin:10px; background: LightGray')
        vbox.append(screen1header)



        myValves = self.SGSConfigurationJSON["Valves"]
        myArray = [('ID', 'Unit Name', 'Valve Number','Control','MS Threshold', 'Time Select', 'Start Time', 'On Time (seconds)')]

            
        # loop through wireless
        for wireless in self.WirelessDeviceJSON:
            myID = wireless["id"]
            myName = wireless["name"]

            for i in range (0,9):
                # first get the description
                myList = []
                myList.append(str(myID))
                myList.append(str(myName))
                currentValve = self.fetchValveJSON(myID, i)
                if len(currentValve) > 0:
                    #print ('currentValve=', currentValve)

                    myList.append(str(currentValve["ValveNumber"]))
                    myList.append(str(currentValve["Control"]))
                    myList.append(str(currentValve["MSThresholdPercent"]))
                    myList.append(str(currentValve["TimerSelect"]))
                    myList.append(str(currentValve["StartTime"]))
                    myList.append(str(currentValve["OnTimeInSeconds"]))
                    myTuple = tuple(myList)
                    myArray.append(myTuple)
                

    
        # set up table display
        #print('myArray=', myArray) 

        self.table = gui.Table.new_from_list(myArray,
                                    width=600, height=400, margin='10px')

        vbox.append(self.table)

        return vbox

    #screen 06
    def buildScreen06(self):


        #screen 06

        vbox = VBox(width=1000, height=510, style="background: LightGray")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        #screen 06

        vbox = self.establishMenu(vbox)



        screen1header = gui.Label("Change Extender Names", style='margin:10px; background: LightGray')
        vbox.append(screen1header)

        items = ()
        for wireless in self.WirelessDeviceJSON:
            myID = wireless["id"]
            myName = wireless["name"]
            item = "wireless:/"+ str(myID) + "/" + str(myName)

            items = items + (item,)

        self.listView2 = gui.ListView.new_from_list(items, width=400, height=25*len(items), margin='10px')
        self.listView2.onselection.do(self.names_list_view_on_selected)
        
        vbox.append(self.listView2)
       


        return vbox

    def names_list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        print("select_item_key=", selected_item_key)
        myUnit =  self.listView2.children[selected_item_key].get_text()

        print("myUnit =", myUnit)
        self.open_input_dialog(widget, myUnit)
        # for on save
        self.current_listView_key = myUnit

        id = myUnit.split("/")[1]
        name = myUnit.split("/")[2]
       

    def open_input_dialog(self, widget, myUnit):

        id = myUnit.split("/")[1]
        name = myUnit.split("/")[2]
        self.renameMyUnit = myUnit
       
        self.inputDialog = gui.InputDialog('Changing '+myUnit, 'New name?',
                                           initial_value=name, 
                                           width=200)
        self.inputDialog.confirm_value.do(
            self.on_input_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def on_input_dialog_confirm(self, widget, value):
        print("value = ", value) 

        id = self.renameMyUnit.split("/")[1]
        name = self.renameMyUnit.split("/")[2]

        # rename unit
        if (len(id) > 1):
        
            newWireless = [] 
            for wireless in self.WirelessDeviceJSON:
                myID = wireless["id"]
                myName = wireless["name"]
                if (str(id) == str(myID)):
                    # we have the record
                    wireless["name"] = value

                    # now write it out to the unit
                    scanForResources.sendNewNameToUnit(wireless["ipaddress"], value)
                newWireless.append(wireless)
            self.WirelessDeviceJSON = newWireless
             
        self.removeAllScreens()
        self.screen06 = self.buildScreen06()
        self.mainContainer.append(self.screen06,'screen06')


    def buildScreen1(self):


        #screen 1

        vbox = VBox(width=1000, height=510, style="background: LightGray")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        #screen 1

        vbox = self.establishMenu(vbox)



        screen1header = gui.Label("Debug / MySQL /MW Tab", style='margin:10px; background: LightGray')
        vbox.append(screen1header)

        #debug config

        debugheader = gui.Label("Debug Configuration", style='position:absolute; left:5px; top:30px; '+self.headerstyle)
        vbox.append(debugheader,'debugheader') 
        self.F_SWDEBUG = gui.CheckBoxLabel( 'enable SW Debugging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_SWDEBUG,'self.F_SWDEBUG') 
       
        # mysql configurattion 
        mysqlheader = gui.Label("MySQL Configuration", style='position:absolute; left:5px; top:40px;'+self.headerstyle)
        vbox.append(mysqlheader,'mysqlheader') 
        self.F_enable_MySQL_Logging = gui.CheckBoxLabel('enable MySQL Logging ', False , height=30, style='margin:5px; background:LightGray')
        self.F_enable_MySQL_Logging.set_value(self.enable_MySQL_Logging)
        vbox.append(self.F_enable_MySQL_Logging,'enable_MySQL_Logging') 

        plabel = gui.Label("MySQL Password", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        self.F_MySQL_Password = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_MySQL_Password.set_value(self.MySQL_Password)
        vbox.append(self.F_MySQL_Password,'MySQLPassword') 


        plabel = gui.Label("SGS Manual and Tank Control", style='position:absolute; left:5px; top:40px;'+self.labelstyle)

        self.F_manual_water = gui.CheckBoxLabel( 'enable Manual Watering', self.manual_water, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_manual_water,'self.F_manual_water') 
        
        plabel = gui.Label("Tank Pump Level", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        self.F_Tank_Pump_Level = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_Tank_Pump_Level.set_value(str(self.Tank_Pump_Level))
        vbox.append(self.F_Tank_Pump_Level,'Tank_Pump_Level') 

        self.F_English_Metric = gui.CheckBoxLabel('Use Metric Units (default English)', False , height=30, style='margin:5px; background:LightGray')
        vbox.append(self.F_English_Metric,'english_metric') 


        return vbox


    def buildScreen2(self):

        #screen 2

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
       
        vbox = self.establishMenu(vbox)
    

        #screen 
        screenheader = gui.Label("Main and Text Notification Tab", style='margin:10px')
        vbox.append(screenheader)
        
        # mail and text notifications
        MTheader = gui.Label("Mail and Text Notification Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(MTheader,'MTheader') 
        

        plabel = gui.Label("Mail Username", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        self.F_mailUser = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_mailUser.set_value(self.mailUser)
        vbox.append(self.F_mailUser,'mailUser') 

        p1label = gui.Label("Mail Password", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p1label,'p1label') 
        
        self.F_mailPassword = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_mailPassword.set_value(self.mailPassword)
        vbox.append(self.F_mailPassword,'mailPassword') 

        p3label = gui.Label("Notify Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p3label,'p3label') 
        
        self.F_notifyAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_notifyAddress.set_value(self.notifyAddress)
        vbox.append(self.F_notifyAddress,'notifyAddress') 

        p4label = gui.Label("From Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p4label,'p4label') 
        
        self.F_fromAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_fromAddress.set_value(self.fromAddress)
        vbox.append(self.F_fromAddress,'fromAddress') 

        self.F_enableText = gui.CheckBoxLabel( 'enable Text Messaging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_enableText,'self.F_enableText') 

        p5label = gui.Label("Text Notify Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label,'p5label') 
        
        self.F_textnotifyAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_textnotifyAddress.set_value(self.textnotifyAddress)
        vbox.append(self.F_textnotifyAddress,'textnotifyAddress') 

        return vbox
    
    def buildScreen3(self):

        #screen 3

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
        
        vbox = self.establishMenu(vbox)
       

       
        #screen 1
        screen1header = gui.Label("Pixel / NeoPixel / SolarMAX Configuration Tab", style='margin:10px')
        vbox.append(screen1header)


        PNheader = gui.Label("Pixel/NeoPixel LED Support", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(PNheader,'PNheader') 

        self.F_enablePixel = gui.CheckBoxLabel( 'Enable Pixel/NeoPixel', self.enablePixel, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_enablePixel,'self.F_enablePixel') 

        P1Nheader = gui.Label("Solar Max Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P1Nheader,'P1Nheader') 

        self.F_SolarMAX_Present = gui.CheckBoxLabel( 'SolarMAX Present', self.SolarMAX_Present, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_SolarMAX_Present,'self.F_SolarMAX_Present') 


        self.F_SolarMAX_Type = gui.DropDown(width='200px')
        self.F_SolarMAX_Type.style.update({'font-size':'large'})
        self.F_SolarMAX_Type.add_class("form-control dropdown")
        item1 = gui.DropDownItem("LEAD")
        item2 = gui.DropDownItem("LIPO")
        self.F_SolarMAX_Type.append(item1,'item1')
        self.F_SolarMAX_Type.append(item2,'item2')
        self.F_SolarMAX_Type.select_by_value(self.SolarMAX_Type)
        vbox.append(self.F_SolarMAX_Type, 'self.F_SolarMAX_Type')

        P2Nheader = gui.Label("Station Height in Meters", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P2Nheader,'P2Nheader') 

        self.F_BMP280_Altitude_Meters = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_BMP280_Altitude_Meters.set_value(str(self.BMP280_Altitude_Meters))
        vbox.append(self.F_BMP280_Altitude_Meters,'BMP280_Altitude_Meters') 

        P3Nheader = gui.Label("Sunlight Gain", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P3Nheader,'P3Nheader') 

        self.F_Sunlight_Gain = gui.DropDown(width='200px')
        self.F_Sunlight_Gain.style.update({'font-size':'large'})
        self.F_Sunlight_Gain.add_class("form-control dropdown")
        item1 = gui.DropDownItem("High")
        item2 = gui.DropDownItem("Low")
        self.F_Sunlight_Gain.append(item1,'item1')
        self.F_Sunlight_Gain.append(item2,'item2')
        if (self.Sunlight_Gain == 0):
            self.F_Sunlight_Gain.select_by_value("Low")
        if (self.Sunlight_Gain == 1):
            self.F_Sunlight_Gain.select_by_value("High")
        vbox.append(self.F_Sunlight_Gain, 'self.F_Sunlight_Gain')




        return vbox

    def buildScreen4(self):
        #screen 4

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        vbox = self.establishMenu(vbox)
   
        #screen 
        screen1header = gui.Label("Weather / WeatherSTEM / WeatherUnderGround Configuration Tab", style='margin:10px')
        vbox.append(screen1header)


        P3_1Nheader = gui.Label("Use Weather", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P3_1Nheader,'P3_1Nheader') 

        self.F_weather = gui.CheckBoxLabel( 'Use Weather', self.weather, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_weather,'self.F_weather') 

        P3Nheader = gui.Label("WeatherSTEM Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P3Nheader,'P3Nheader') 

        self.F_USEWEATHERSTEM = gui.CheckBoxLabel( 'Enable WeatherSTEM', self.USEWEATHERSTEM, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_USEWEATHERSTEM,'self.F_USEWEATHERSTEM') 

        p5label = gui.Label("Interval between pictures (seconds)", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label,'p5label') 
        
        self.F_INTERVAL_CAM_PICS__SECONDS = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_INTERVAL_CAM_PICS__SECONDS.set_value(str(self.INTERVAL_CAM_PICS__SECONDS))
        vbox.append(self.F_INTERVAL_CAM_PICS__SECONDS,'INTERVAL_CAM_PICS__SECONDS') 

        p6label = gui.Label("GardenCam Station Key", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p6label,'p6label') 
        
        self.F_STATIONKEY = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_STATIONKEY.set_value(str(self.STATIONKEY))
        vbox.append(self.F_STATIONKEY,'STATIONKEY') 

        #

        P4Nheader = gui.Label("WeatherUnderGround Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P4Nheader,'P4Nheader') 
        
        self.F_WeatherUnderground_Present = gui.CheckBoxLabel( 'Enable WeatherUnderground', self.WeatherUnderground_Present, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_WeatherUnderground_Present,'self.F_WeatherUnderground_Present') 

        p7label = gui.Label("Station ID", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p7label,'p7label') 
        
        self.F_WeatherUnderground_StationID = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_WeatherUnderground_StationID.set_value(self.WeatherUnderground_StationID)
        vbox.append(self.F_WeatherUnderground_StationID,'WeatherUnderground_StationID') 

        p8label = gui.Label("Station Key", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p8label,'p8label') 
        
        self.F_WeatherUnderground_StationKey = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_WeatherUnderground_StationKey.set_value(self.WeatherUnderground_StationKey)
        vbox.append(self.F_WeatherUnderground_StationKey,'WeatherUnderground_StationKey') 

        return vbox

    def buildScreen5(self):
        #screen 5

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        vbox = self.establishMenu(vbox)
   
   

        #screen 1
        screen1header = gui.Label("Blynk / ThunderBoard AS3935 Tab", style='margin:10px')
        vbox.append(screen1header)



        P5Nheader = gui.Label("Blynk Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 

        self.F_USEBLYNK = gui.CheckBoxLabel( 'Enable Blynk', self.USEBLYNK, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_USEBLYNK,'self.F_USEBLYNK') 

        p8label = gui.Label("Blynk App Authorization", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p8label,'p8label') 
        
        self.F_BLYNK_AUTH = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_BLYNK_AUTH.set_value(self.BLYNK_AUTH)
        vbox.append(self.F_BLYNK_AUTH,'BLYNK_AUTH') 
        #
        P1Nheader = gui.Label("ThunderBoard AS3935 Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P1Nheader,'P1Nheader') 

        P2Nheader = gui.Label("Format:[NoiseFloor, Indoor, TuneCap, DisturberDetection, WatchDogThreshold, SpikeDetection] ", style='position:absolute; left:5px; top:30px;'+self.labelstyle)
        vbox.append(P2Nheader,'P2Nheader') 
        

        p9label = gui.Label("Thunderboard Configuration", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p9label,'p9label') 
        
        self.F_AS3935_Lightning_Config  = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_AS3935_Lightning_Config .set_value(self.AS3935_Lightning_Config )
        vbox.append(self.F_AS3935_Lightning_Config ,'AS3935_Lightning_Config ') 


        return vbox

    def buildScreen6(self):
        #screen 6

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        vbox = self.establishMenu(vbox)
   

        #screen 
        screenheader = gui.Label("Pin Config Tab", style='margin:10px')
        vbox.append(screenheader)
        
        # short headers

        shortlabelstyle = 'font-family:monospace; width:200; font-size:15px; margin:5px; background:LightGray' 



        P5Nheader = gui.Label("Pin Configurations", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 

        p8label = gui.Label("Ultrasonic Pin ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p8label,'p8label') 
        
        self.F_UltrasonicLevel = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_UltrasonicLevel.set_value(str(self.UltrasonicLevel))
        vbox.append(self.F_UltrasonicLevel,'UltrasonicLevel') 

        p1label = gui.Label("Pixel Pin", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p1label,'p1label') 
        self.F_pixelPin = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_pixelPin.set_value(str(self.pixelPin))
        vbox.append(self.F_pixelPin,'pixelPin') 
        

        return vbox


    def buildScreen7(self):
        #screen 7

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        vbox = self.establishMenu(vbox)

        #screen 
        screenheader = gui.Label("Camera / MQTT / Rest Tab", style='margin:10px')
        vbox.append(screenheader)
        
        # short headers

        shortlabelstyle = 'font-family:monospace; width:200; font-size:15px; margin:5px; background:LightGray' 



        P5Nheader = gui.Label("Night Camera Enable", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 
        self.F_Camera_Night_Enable = gui.CheckBoxLabel( 'Night Vision Enable', self.Camera_Night_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_Camera_Night_Enable,'self.F_Camera_Night_Enable') 

        P7Nheader = gui.Label("REST Interface", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P7Nheader,'P7Nheader') 
        self.F_REST_Enable = gui.CheckBoxLabel( 'REST Enable', self.REST_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_REST_Enable,'self.F_REST_Enable') 


        P6Nheader = gui.Label("MQTT Configuration (SGS OUT to other broker)", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P6Nheader,'P6Nheader') 

        self.F_MQTT_Enable = gui.CheckBoxLabel( 'MQTT Enable', self.MQTT_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_MQTT_Enable,'self.F_MQTT_Enable') 

        p4label = gui.Label("MQTT Server URL ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p4label,'p4label') 
        
        self.F_MQTT_Server_URL = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Server_URL.set_value(self.MQTT_Server_URL)
        vbox.append(self.F_MQTT_Server_URL,'MQTT_Server_URL') 

        p3label = gui.Label("MQTT Server Port Number ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p3label,'p3label') 
        
        self.F_MQTT_Port_Number = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Port_Number.set_value(str(self.MQTT_Port_Number))
        vbox.append(self.F_MQTT_Port_Number,'MQTT_Port_Number') 

        p2label = gui.Label("How Often MQTT Sent in Seconds ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p2label,'p2label') 
        
        self.F_MQTT_Send_Seconds = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Send_Seconds.set_value(str(self.MQTT_Send_Seconds))
        vbox.append(self.F_MQTT_Send_Seconds,'MQTT_Send_Seconds') 





        return vbox



    def main(self):

        self.readJSON()
        self.readJSONSGSConfiguration()

        #this flag will be used to stop the display_counter Timer
        self.stop_flag = True 
        self.count = 0
        self.ScanRunning = False
        self.SFHWorking = False
        # progress counter 
        self.progress = gui.Progress(1, 100, width=200, height=30, style='margin: 10px')

        # kick off regular display of counter
        self.display_counter() 

        # GUI default information
        self.dropDownValveSelected = "None"





        widthBox = 1000
        heightBox = 900
        self.mainContainer = Container(width=widthBox, height=heightBox, margin='0px auto', style="position: relative")
        self.mainContainer.style['justify-content'] = 'flex-start'
        self.mainContainer.style['align-items'] = 'flex-start'


        logo = SuperImage("./static/SGfulllogocolor.png", width=400, height =142)
        header = gui.Label("Smart Garden System Configuration Tool V003", style='position:absolute; left:150px; top:120px')
        # bottom buttons

        cancel = gui.Button('Cancel',style='position:absolute; left:550px; height: 30px; width:100px; margin:10px; top:5px')
        cancel.onclick.do(self.onCancel)
        save = gui.Button('Save',style='position:absolute; left:400px; height: 30px; width:100px;  margin: 10px;  top:5px')
        save.onclick.do(self.onSave)
        saveandreload = gui.Button('Save and Reload SGS',style='position:absolute; left:675px; height: 30px; width:100px;  margin: 10px;  top:5px')
        saveandreload.onclick.do(self.onSaveAndReloadSGS)
        exit = gui.Button('Save and Exit',style='position:absolute; left:500px; height: 30px; width:100px;  margin: 10px;  top:95px')
        exit.onclick.do(self.onExit)
        reset = gui.Button('Reset to Defaults',style='position:absolute; left:400px;height: 30px;   width:250px; margin: 10px; top:50px')
        reset.onclick.do(self.onReset)
        # appending a widget to another
        self.mainContainer.append(logo)
        self.mainContainer.append(header)
        self.mainContainer.append(cancel)
        self.mainContainer.append(save)
        self.mainContainer.append(saveandreload)
        self.mainContainer.append(exit)
        self.mainContainer.append(reset)


        # configuation fields
       

        self.headerstyle= 'width:400px; font-family:monospace; font-size:20px; margin:10px; background:LightBlue'
        self.labelstyle = 'font-family:monospace; font-size:15px; margin:5px; background:LightGray' 

        # build screens


        self.screen0 = self.buildScreen0()
        self.screen05 = self.buildScreen05()
        self.screen06 = self.buildScreen06()
        self.screen1 = self.buildScreen1()
        self.screen2 = self.buildScreen2()
        self.screen3 = self.buildScreen3()
        self.screen4 = self.buildScreen4()
        self.screen5 = self.buildScreen5()
        self.screen6 = self.buildScreen6()
        self.screen7 = self.buildScreen7()


        self.mainContainer.append(self.screen0,'screen0')
        



        # returning the root widget
        
        return self.mainContainer


    # listener functions


    def removeAllScreens(self):
        
        self.mainContainer.remove_child(self.screen0)
        self.mainContainer.remove_child(self.screen05)
        self.mainContainer.remove_child(self.screen06)
        self.mainContainer.remove_child(self.screen1)
        self.mainContainer.remove_child(self.screen2)
        self.mainContainer.remove_child(self.screen3)
        self.mainContainer.remove_child(self.screen4)
        self.mainContainer.remove_child(self.screen5)
        self.mainContainer.remove_child(self.screen6)
        self.mainContainer.remove_child(self.screen7)
        
    # listener functions

    def menu_screen0_clicked(self, widget):
        self.removeAllScreens()
        self.screen0 = self.buildScreen0()
        self.mainContainer.append(self.screen0,'screen0')
        print("menu screen0 clicked")  

    def menu_screen05_clicked(self, widget):
        self.removeAllScreens()
        self.screen05 = self.buildScreen05()
        self.mainContainer.append(self.screen05,'screen05')
        print("menu screen05 clicked")  

    def menu_screen06_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen06,'screen06')
        print("menu screen06 clicked")  

    def menu_screen1_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen1,'screen1')
        print("menu screen1 clicked")  

    def menu_screen2_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen2,'screen2')
        print("menu screen2 clicked")

    def menu_screen3_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen3,'screen3')
        print("menu screen3 clicked")

    def menu_screen4_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen4,'screen4')
        print("menu screen4 clicked")

    def menu_screen5_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen5,'screen5')
        print("menu screen5 clicked")

    def menu_screen6_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen6,'screen6')
        print("menu screen6 clicked")


    def menu_screen7_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen7,'screen7')
        print("menu screen7 clicked")

    # scanning sofrware

    def ScanForHardware(self, widget, name='', surname=''):
        print("self.SFHWorking =", self.SFHWorking)
        # disable menu
        self.menubar.set_enabled(False)
        if (self.SFHWorking == False): 
            self.SFHWorking = True
            SFHThread = threading.Thread(target=self.ScanForHardwareWorker, args=('name',))

            SFHThread.start()
    

    def ScanForHardwareWorker(self, name): 
       

        print ("Scanning for Hardware")
        self.stop_flag = False
        
        
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

    
            self.count = self.count+1
            self.Display_IP.set_text('Scanning IP: ' + str(ip))
            self.Display_WEXT.set_text('Found Wireless Extenders: '+ str(len(returnJSON)))
            JSON = "" 
            JSON = scanForResources.checkForDeviceFromIP(ip)
            #print("JSON=", JSON)
            #print("JSONLength=", len(JSON))
            if len(JSON) != 0 :
                print("JSON=", JSON)
                # check for SGS JSON
                #print("JSON[1]=", JSON[1])
             
                #DumpedJSON = json.dumps(JSON)
                #DumpedJSON = json.loads(JSON)
                #print("DumpedJOSN =", DumpedJSON)
                try:
                    if (len(JSON["id"]) == 4):
                        if (len(JSON["return_string"]) > 0):
                            print ("SGS Wireless Extender Found.  ID=", JSON["id"])
                            returnJSON.append(JSON)

                except:
                    #traceback.print_exc()
                    pass
            
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Finish Time =", str(now))
        print ("returnJSON", returnJSON)
      
        self.WirelessDeviceJSON = returnJSON

        self.WirelessDeviceJSON = returnJSON
        self.mainContainer.remove_child(self.screen0)
        self.screen0 = self.buildScreen0()
        self.mainContainer.append(self.screen0,'screen0')
       
        self.progress.set_value(100)
        self.menubar.set_enabled(True)
        self.SFHWorking = False
    # Buttons

    def onCancel(self, widget, name='', surname=''):
        print("onCancel clicked")
        self.server.server_starter_instance._alive = False
        self.server.server_starter_instance._sserver.shutdown()
        print("server stopped") 
        exit()
        
    def onExit(self, widget, name='', surname=''):
        # save and exit
        print("onSaveExit clicked")
        self.saveJSON()
        self.saveSGSConfigurationJSON()
        self.server.server_starter_instance._alive = False
        self.server.server_starter_instance._sserver.shutdown()
        print("server stopped") 
        exit()

    def onReset(self, widget, name='', surname=''):
        print("Reset clicked")
        self.removeAllScreens()
        self.mainContainer.append(self.screen1,'screen1')
        self.setDefaults()

        self.screen0 = self.buildScreen0()
        self.screen05 = self.buildScreen05()
        self.screen06 = self.buildScreen06()
        self.screen1 = self.buildScreen1()
        self.screen2 = self.buildScreen2()
        self.screen3 = self.buildScreen3()
        self.screen4 = self.buildScreen4()
        self.screen5 = self.buildScreen5()
        self.screen6 = self.buildScreen6()
        self.screen7 = self.buildScreen7()


        self.mainContainer.append(self.screen1,'screen1')
        
        
    def onSave(self, widget, name='', surname=''):
        print("onSave clicked")
        self.saveJSON()
        self.saveSGSConfigurationJSON()

        
    def onSaveAndReloadSGS(self, widget, name='', surname=''):
        print("onSave and Reload SGS clicked")
        self.saveJSON()
        self.saveSGSConfigurationJSON()
        fname = 'NEWJSON'
        with open(fname, 'a'):
            try:                     # Whatever if file was already existing
                os.utime(fname, None)  # => Set current time anyway
            except OSError:
                pass  # File deleted between open() and os.utime() call

#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 8001, 'config_address': '0.0.0.0', 'config_start_browser': False, 'config_project_name': 'SGS Configuration', 'config_resourcepath': './res/'}

# starts the web server
#start(SGSConfigure, address='0.0.0.0', port=8001)

start(SGSConfigure, address=configuration['config_address'], port=configuration['config_port'],
                        multiple_instance=configuration['config_multiple_instance'],
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
