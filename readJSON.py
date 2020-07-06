import config
import json
import os



def readJSONSGSConfiguration(addPath):
        if os.path.isfile(addPath+'SGSConfiguration.JSON'):
            print (addPath+"SGSConfiguration.JSON File exists")
            with open(addPath+'SGSConfiguration.JSON') as json_file:
                JSONData = json.load(json_file)
                #print("JSONData from SGSConfigFile=", JSONData)
                config.SGSConfigurationJSON  = JSONData 
        else:
            print (addPath+"SGSConfiguration.JSON File does not exist")
            config.SGSConfigurationJSON = {"SGSConfigVersion": "001",
                                        "Valves":  [] 
                                        }
            #print("Default JSONData for SGSConfigFile=", config.SGSConfigurationJSON)
            JSONsetDefaults()

        
def readJSON(addPath):

        JSONsetDefaults()

        if os.path.isfile(addPath+'SGS.JSON'):
            print (addPath+"SGS.JSON File exists")
            with open(addPath+'SGS.JSON') as json_file:
                config.JSONData = json.load(json_file)


                #print("JSONData from File=", config.JSONData)
                config.SWDEBUG = getJSONValue('SWDEBUG')
                config.enable_MySQL_Logging = getJSONValue('enable_MySQL_Logging')
                config.English_Metric = getJSONValue('English_Metric')
                config.MySQL_Password = getJSONValue('MySQL_Password')
                config.mailUser = getJSONValue('mailUser')
                config.mailPassword = getJSONValue('mailPassword')
                config.notifyAddress = getJSONValue('notifyAddress')
                config.fromAddress = getJSONValue('fromAddress')
                config.enableText = getJSONValue('enableText')
                config.textnotifyAddress = getJSONValue('textnotifyAddress')
                config.enablePixel = getJSONValue('enablePixel')
                config.pixelPin = getJSONValue('pixelPin')
                config.SolarMAX_Present = getJSONValue('SolarMAX_Present')
                config.SolarMAX_Type = getJSONValue('SolarMAX_Type')
                config.BMP280_Altitude_Meters = getJSONValue('BMP280_Altitude_Meters')
                config.Sunlight_Gain = getJSONValue('Sunlight_Gain')
                config.weather = getJSONValue('weather')
                config.USEWEATHERSTEM = getJSONValue('USEWEATHERSTEM')
                config.INTERVAL_CAM_PICS__SECONDS = getJSONValue('INTERVAL_CAM_PICS__SECONDS')
                config.STATIONKEY = getJSONValue('STATIONKEY')
                config.WeatherUnderground_Present = getJSONValue('WeatherUnderground_Present')
                config.WeatherUnderground_StationID = getJSONValue('WeatherUnderground_StationID')
                config.WeatherUnderground_StationKey = getJSONValue('WeatherUnderground_StationKey')
                config.USEBLYNK = getJSONValue('USEBLYNK')
                config.BLYNK_AUTH = getJSONValue('BLYNK_AUTH')
                config.AS3935_Lightning_Config = getJSONValue('AS3935_Lightning_Config')
                config.Camera_Night_Enable = getJSONValue('Camera_Night_Enable')
                config.REST_Enable = getJSONValue('REST_Enable')
                config.MQTT_Enable = getJSONValue('MQTT_Enable')
                config.MQTT_Server_URL = getJSONValue('MQTT_Server_URL')
                config.MQTT_Port_Number = getJSONValue('MQTT_Port_Number')
                config.MQTT_Send_Seconds = getJSONValue('MQTT_Send_Seconds')
                config.UltrasonicLevel = getJSONValue('UltrasonicLevel') 
                config.Tank_Pump_Level = getJSONValue('Tank_Pump_Level') 
                config.manual_water = getJSONValue('manual_water') 
                config.WirelessDeviceJSON = getJSONValue('WirelessDeviceJSON') 
                #print("WirelessDeviceJSON Read from file", config.WirelessDeviceJSON)
        else:
            print ("SGS.JSON File does not exist")
            JSONsetDefaults()



    
def JSONsetDefaults():
        config.SWDEBUG = False
        config.enable_MySQL_Logging = False
        config.English_Metric = False
        config.MySQL_Password = "password"
        config.mailUser = "yourusername"
        config.mailPassword = "yourmailpassword"
        config.notifyAddress = "you@example.com"
        config.fromAddress = "yourfromaddress@example.com"
        config.enableText = False
        config.textnotifyAddress = "yournumber@yourprovider"
        config.enablePixel = False
        config.pixelPin = 21
        config.SolarMAX_Present = False
        config.SolarMAX_Type = "LEAD"
        config.BMP280_Altitude_Meters = 626.0
        config.Sunlight_Gain = 0
        config.weather = False
        config.USEWEATHERSTEM = False
        config.INTERVAL_CAM_PICS__SECONDS = 60
        config.STATIONKEY = ""
        config.WeatherUnderground_Present = False
        config.WeatherUnderground_StationID = "KWXXXXX"
        config.WeatherUnderground_StationKey = "YYYYYY"
        config.USEBLYNK = False
        config.BLYNK_AUTH = ""
        config.AS3935_Lightning_Config = "[2,1,3,0,3,3]"
        config.Camera_Night_Enable =  False
        config.REST_Enable = False 
        config.MQTT_Enable = False 
        config.MQTT_Server_URL = "" 
        config.MQTT_Port_Number = 5900 
        config.MQTT_Send_Seconds = 500 
        config.UltrasonicLevel = 4
        config.Tank_Pump_Level = 15.0
        config.manual_water = True
        config.WirelessDeviceJSON = ""

       
        config.dataDefaults = {} 

        config.dataDefaults['SWDEBUG'] = config.SWDEBUG 
        config.dataDefaults['enable_MySQL_Logging'] = config.enable_MySQL_Logging 
        config.dataDefaults['English_Metric'] = config.English_Metric 
        config.dataDefaults['MySQL_Password'] = config.MySQL_Password 
        config.dataDefaults['mailUser'] = config.mailUser 
        config.dataDefaults['mailPassword'] = config.mailPassword 
        config.dataDefaults['notifyAddress'] = config.notifyAddress 
        config.dataDefaults['fromAddress'] = config.fromAddress 
        config.dataDefaults['enableText'] = config.enableText 
        config.dataDefaults['textnotifyAddress'] = config.textnotifyAddress 
        config.dataDefaults['enablePixel'] = config.enablePixel 
        config.dataDefaults['pixelPin'] = config.pixelPin 
        config.dataDefaults['SolarMAX_Present'] = config.SolarMAX_Present 
        config.dataDefaults['SolarMAX_Type'] = config.SolarMAX_Type 
        config.dataDefaults['BMP280_Altitude_Meters'] = config.BMP280_Altitude_Meters 
        config.dataDefaults['Sunlight_Gain'] = config.Sunlight_Gain 
        config.dataDefaults['weather'] = config.weather 
        config.dataDefaults['USEWEATHERSTEM'] = config.USEWEATHERSTEM 
        config.dataDefaults['INTERVAL_CAM_PICS__SECONDS'] = config.INTERVAL_CAM_PICS__SECONDS 
        config.dataDefaults['STATIONKEY'] = config.STATIONKEY 
        config.dataDefaults['WeatherUnderground_Present'] = config.WeatherUnderground_Present 
        config.dataDefaults['WeatherUnderground_StationID'] = config.WeatherUnderground_StationID 
        config.dataDefaults['WeatherUnderground_StationKey'] = config.WeatherUnderground_StationKey 
        config.dataDefaults['USEBLYNK'] = config.USEBLYNK 
        config.dataDefaults['BLYNK_AUTH'] = config.BLYNK_AUTH 
        config.dataDefaults['AS3935_Lightning_Config'] = config.AS3935_Lightning_Config 
        config.dataDefaults['REST_Enable'] = config.REST_Enable 
        config.dataDefaults['MQTT_Enable'] = config.MQTT_Enable 
        config.dataDefaults['MQTT_Server_URL'] = config.MQTT_Server_URL 
        config.dataDefaults['MQTT_Port_Number'] = config.MQTT_Port_Number 
        config.dataDefaults['MQTT_Send_Seconds'] = config.MQTT_Send_Seconds 
        config.dataDefaults['UltrasonicLevel'] = config.UltrasonicLevel
        config.dataDefaults['Tank_Pump_Level'] = config.Tank_Pump_Level 
        config.dataDefaults['manual_water'] = config.manual_water 
        config.dataDefaults['WirelessDeviceJSON'] = config.WirelessDeviceJSON 
        

       
       
def getJSONValue( entry):
        try:
            returnData = config.JSONData[entry]
            return returnData
        except:
            print("JSON value not found - Set to Defaults:", entry)
            return config.dataDefaults[entry]




