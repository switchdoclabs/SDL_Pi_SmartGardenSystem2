

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.express as px 
import plotly.graph_objs as go

import datetime
import traceback
import sys

# SGS imports
sys.path.append("../")

import state
import config
import readJSON
import json

headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'

# read JSON

readJSON.readJSON("../")
readJSON.readJSONSGSConfiguration("../")

import MySQLdb as mdb

def getDayDelay(DOWCoverage, currentDayOfWeek):
    
    if (DOWCoverage[currentDayOfWeek] == "Y"):
        return 0
    delay = 0
    for i in range(0,6):
       nextDay = (currentDayOfWeek +i ) % 7
       print("currentDayOfWeek =", currentDayOfWeek, i)
       if (DOWCoverage[nextDay] == "Y"):
        return delay
       else:
        delay = delay+1
    return delay
        
def checkDOWCoverage(DOWCoverage):
    if (DOWCoverage == "NNNNNNN"):
        return False
    return True


def getTimeDelta(timerValue, DOWCoverage):




    timeDelta = datetime.timedelta(minutes=15)
    # calculate DWO coverage difference
    #currentDayOfWeek = int(datetime.datetime.today().strftime('%w'))
    # 0 is Sunday

    #dayDelay = getDayDelay(DOWCoverage, currentDayOfWeek) 
    #print("dayDelay=", dayDelay)
    dayDelay = 0

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
    return timeDelta + datetime.timedelta(days=dayDelay)


################
# p_v Page
################
def buildTableFig(myData, title):
    #print("myData=", myData)
    if (title=="Next Scheduled Events"):
        fig = go.Figure(data=[
		go.Table(
                   columnwidth = [300,100,150,200,150,100,300],
                   header = dict(
                     values = [
                                   ['<b>Next Scheduled</b>'], 
                                   ['<b>On Time (Seconds)</b>'],
                                   ['<b>ID</b>'], 
                                   ['<b>Unit Name</b>'],
                                   ['<b>Valve Number</b>'],
                                   ['<b>Day of Week Coverage (Su-Sa)</b>'],
                                   ['<b>Control</b>'],
                                   ],
                     line_color='darkslategray',
                     fill_color='royalblue',
                     align=['left','center'],
                     font=dict(color='white', size=12),
                     height=40
                   ),
                   cells=dict(
                     values=myData,
                     line_color='darkslategray',
                     # 2-D list of colors for alternating rows
                     fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor]*10],
                     fill=dict(color=['paleturquoise', 'white']),
                     align=['left', 'center'],
                     font_size=12,
                     height=30),
                     ) 
		 ],
		 layout= {"title" : title, "autosize" : True, "height" : 1500},
                     )
        return fig
	
	
    return fig

         
        
def fetchValveJSON(myID, valveNumber):
       
        # read JSON

        readJSON.readJSON("../")
        readJSON.readJSONSGSConfiguration("../")

        myJSON=config.SGSConfigurationJSON

        #print("myJSON=", myJSON) 
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
        
def fetchProgramming():
    myArray = []

    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
    print("wirelessJSON = ", wirelessJSON)
    nextScheduleList = []
    myTimeOn = []
    myIDList = []
    myNameList = []
    myValveNumberList = []
    myDOWCoverageList = []
    myControlList = []

    for wireless in wirelessJSON:
        myID = wireless["id"]
        myName = wireless["name"]


        for i in range (1,9):
                myIDList.append(str(myID))
                myNameList.append(str(myName))
                currentValve = fetchValveJSON(myID, i)
                if len(currentValve) > 0:
                    #print ('currentValve=', currentValve)
                    myControl = currentValve["Control"]
                    DOWNever = ""
                    if (currentValve["DOWCoverage"] == "NNNNNNN"):
                       DOWNever = "(COW: Never)" 
                    if (myControl[0:2] == "MS"):   # found Moisture sensor
                        nextScheduleList.append("Moisture Sensor " + DOWNever)
                    else:
                        if (myControl[0:3] == "Off"):   # found Moisture sensor
                            nextScheduleList.append("Off")
                        else:
                            myTempTime = currentValve["StartTime"].split(":")
                            NextTime = datetime.datetime.now() - datetime.timedelta(days=1) 
                            # if DOWCoverage current DOW is "N" then advance one day
                            currentDayOfWeek = int(datetime.datetime.today().strftime('%w'))
                            if (currentValve["DOWCoverage"][currentDayOfWeek] == "N"):
                                NextTime = NextTime - datetime.timedelta(days=1)
                            NextTime = NextTime.replace(hour=int(myTempTime[0]), minute=int(myTempTime[1]),second=0,microsecond=0)

                            dayDelay = getDayDelay(currentValve["DOWCoverage"], currentDayOfWeek) 
                            if (dayDelay > 0):
                                nowTime = datetime.datetime.now() + datetime.timedelta(days=dayDelay)
                                nowTime = nowTime.replace(hour=int(myTempTime[0]), minute=int(myTempTime[1]),second=0,microsecond=0)
                            else:
                                 nowTime = datetime.datetime.now() 
                        
                            if (NextTime <= nowTime):
        
                                #set up next fire
                                timeDelta = getTimeDelta(currentValve["TimerSelect"], currentValve["DOWCoverage"])
                                while NextTime < nowTime:
                                    NextTime = NextTime + timeDelta
                                myNextTime = NextTime.strftime('%Y-%m-%d %H:%M:%S')
 
                                if (currentValve["DOWCoverage"] == "NNNNNNN"):
                                    DOWNever = "COW: Never" 
                                    nextScheduleList.append(DOWNever)
                                else:
                                    nextScheduleList.append(myNextTime)
                        
                    myTimeOn.append(str(currentValve["OnTimeInSeconds"]))
                    myValveNumberList.append(str(currentValve["ValveNumber"]))
                    myDOWCoverageList.append(str(currentValve["DOWCoverage"]))
                    myControlList.append(str(currentValve["Control"]))
                

    myArray.append( nextScheduleList)
    myArray.append( myTimeOn)
    myArray.append( myIDList)
    myArray.append(myNameList)
    myArray.append(myValveNumberList)
    myArray.append(myDOWCoverageList)
    myArray.append(myControlList)
    #print('myArray=', myArray) 

    return myArray

def updateProgramming(): 
      layout = [] 
      data = fetchProgramming()
      fig = buildTableFig(data,"Next Scheduled Events")
      #print("upProgfig=", fig)
      layout.append(dcc.Graph(id={"type": "VSdynamic", "index": "pvprogramming"},figure=fig, ))	

      return layout

################
# Page Functions
################


def ValvesScheduledPage():
    Row1 = html.Div(
        [ html.H1(children="Next Events"),
            #dbc.Row(
                #[
			html.Div(updateProgramming())
                #]
            #),
        ]
    )
    #layout = dbc.Container([
    layout = dbc.Container([
        Row1],
        className="p-5",
    )
    return layout







