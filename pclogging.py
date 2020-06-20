from __future__ import print_function
#
#
# logging system from Project Curacao 
# filename: pclogger.py
# Version 1.0 10/04/13
#
# contains logging data 
#



import sys
import time
# Check for user imports
import config

import state

import MySQLdb as mdb


import traceback


def systemlog(level,  message):


 if (config.enable_MySQL_Logging == True):	
   LOWESTDEBUG = 0
	# open mysql database
	# write log
	# commit
	# close

   if (level >= LOWESTDEBUG):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                #print "before query"
                query = "INSERT INTO SystemLog(TimeStamp, Level, SystemText ) VALUES(LOCALTIMESTAMP(), %i, '%s')" % (level, message)
                print("query=%s" % query)
                cur.execute(query)
                con.commit()


        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)
        finally:
                cur.close()
                con.close()

                del cur
                del con



def sensorlog(DeviceID, SensorNumber, SensorValue, SensorType, TimeRead ):
 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                query = "INSERT INTO Sensors(DeviceID, SensorNumber, SensorValue, SensorType, TimeRead ) VALUES('%s', '%s', %f, '%s', '%s')" % (DeviceID, SensorNumber, float(SensorValue), SensorType, TimeRead)
                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con




def valvelog(DeviceID, ValveNumber, State, Source, ValveType, Seconds):
 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                query = "INSERT INTO ValveChanges(DeviceID, ValveNumber, State, Source, ValveType, SecondsOn ) VALUES('%s', '%s', %d, '%s', '%s',%d)" % (DeviceID, ValveNumber, int(State), Source, ValveType, int(Seconds))
                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con


def writeMQTTValveChangeRecord(MQTTJSON):

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                query = "INSERT INTO ValveRecord(DeviceID, State) VALUES('%s', '%s')" % (MQTTJSON['id'], MQTTJSON['valvestate'])
                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con


def writeWeatherRecord():

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                fields = "OutdoorTemperature, OutdoorHumidity, IndoorTemperature, IndoorHumidity, TotalRain, SunlightVisible, SunlightUVIndex, WindSpeed, WindGust, WindDirection,BarometricPressure, BarometricPressureSeaLevel, BarometricTemperature, AQI"
                values = "%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%6.2f,%6.2f" % (state.OutdoorTemperature, state.OutdoorHumidity, state.IndoorTemperature, state.IndoorHumidity, state.TotalRain, state.SunlightVisible, state.SunlightUVIndex, state.WindSpeed, state.WindGust, state.WindDirection,state.BarometricPressure, state.BarometricPressureSeaLevel, state.BarometricTemperature, state.AQI)
                query = "INSERT INTO WeatherData (%s) VALUES(%s )" % (fields, values)
                print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con



