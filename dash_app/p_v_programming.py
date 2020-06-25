

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



################
# p_v Page
################
def buildTableFig(myData, title):
    print("myData=", myData)
    if (title=="Pump and Valve Programming"):
        fig = go.Figure(data=[
		go.Table(
                   columnwidth = [150,200,150,500,150,150,150,150,150 ],
                   header = dict(
                     values = [['<b>ID</b>'], ['<b>Unit Name</b>'],
                                   ['<b>Valve Number</b>'],
                                   ['<b>Control</b>'],
                                   ['<b>MS Threshold</b>'],
                                   ['<b>Time Select</b>'],
                                   ['<b>Start Time</b>'],
                                   ['<b>On Time (Seconds)</b>'],
                                   ['<b>Show Graph</b>'],
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
	
	
    fig = html.H1(children="Error in print system log")


         
        
def fetchValveJSON(myID, valveNumber):
       
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
    myIDList = []
    myNameList = []
    myValveNumberList = []
    myControlList = []
    myMSThresholdPercentList = []
    myTimerSelectList = []
    myStartTimeList = []
    myOnTimeInSecondsList = []
    myShowGraphList = []

    for wireless in wirelessJSON:
        myID = wireless["id"]
        myName = wireless["name"]
        '''
        for i in range (0,9):
                myList = []
                myList.append(str(myID))
                myList.append(str(myName))
                currentValve = fetchValveJSON(myID, i)
                if len(currentValve) > 0:
                    #print ('currentValve=', currentValve)

                    myList.append(str(currentValve["ValveNumber"]))
                    myList.append(str(currentValve["Control"]))
                    myList.append(str(currentValve["MSThresholdPercent"]))
                    myList.append(str(currentValve["TimerSelect"]))
                    myList.append(str(currentValve["StartTime"]))
                    myList.append(str(currentValve["OnTimeInSeconds"]))
                    myList.append(str(currentValve["ShowGraph"]))
                    myTuple = tuple(myList)
                    myArray.append(myTuple)
        '''


        for i in range (1,9):
                myIDList.append(str(myID))
                myNameList.append(str(myName))
                currentValve = fetchValveJSON(myID, i)
                if len(currentValve) > 0:
                    #print ('currentValve=', currentValve)

                    myValveNumberList.append(str(currentValve["ValveNumber"]))
                    myControlList.append(str(currentValve["Control"]))
                    myMSThresholdPercentList.append(str(currentValve["MSThresholdPercent"]))
                    myTimerSelectList.append(str(currentValve["TimerSelect"]))
                    myStartTimeList.append(str(currentValve["StartTime"]))
                    myOnTimeInSecondsList.append(str(currentValve["OnTimeInSeconds"]))
                    myShowGraphList.append(str(currentValve["ShowGraph"]))
                

    myArray.append( myIDList)
    myArray.append(myNameList)
    myArray.append(myValveNumberList)
    myArray.append(myControlList)
    myArray.append(myMSThresholdPercentList) 
    myArray.append(myTimerSelectList) 
    myArray.append(myStartTimeList) 
    myArray.append(myOnTimeInSecondsList) 
    myArray.append(myShowGraphList) 
    # set up table display
    print('myArray=', myArray) 

    return myArray

def updateProgramming(): 
      layout = [] 
      data = fetchProgramming()
      fig = buildTableFig(data,"Pump and Valve Programming")
      print("fig=", fig)
      layout.append(dcc.Graph(id={"type": "PVPdynamic", "index": "pvprogramming"},figure=fig, ))	

      return layout

################
# Page Functions
################


def PVProgrammingPage():
    Row1 = html.Div(
        [ html.H1(children="PV Programming"),
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







