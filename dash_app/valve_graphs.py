


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



# read JSON

readJSON.readJSON("../")
readJSON.readJSONSGSConfiguration("../")

import MySQLdb as mdb



def fetchCurrentValveData(myID, ValveNumber, timeDelta):

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT TimeStamp, State FROM ValveRecord WHERE ( (DeviceID = '%s') AND  (TimeStamp > '%s') ) ORDER BY TimeStamp DESC " % (myID, before)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #if (ValveNumber == 0):
                #     print ("Query records=", records)
                return records
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

################
# Valve Graphs
################


def getNameFromID(myID):
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        for singleWireless in wirelessJSON:
            if (str(myID).replace(" ","")  == str(singleWireless["id"]).replace(" ","")):
                return singleWireless["name"]
        return "Inactive"

        

    
def fullDisplayGraphs():
    Graphs = []

    myValves = config.SGSConfigurationJSON["Valves"]
    
    columnCount = 0
    for single in myValves:
        
        if (single["ShowGraph"] == True):
            #print("valve=", single)
            timeDelta = datetime.timedelta(days = 1) 
            singleGraph = returnaGraph(single, timeDelta)
            Graphs.append(singleGraph)
    return Graphs

def returnValveValue(state, number):
    #print("state=%s:%d"%( state, number))
    if (state[number] == "0"):
        return "OFF"
    else:
        return "ON"


def returnaFig(myID, ValveNumber ,Time, Y, extra):
    myName = getNameFromID(myID)  
    print("myName=", myName, myID)
    if (myName == "Inactive"):
        fig = go.Figure( layout=go.Layout(
                                   title = go.layout.Title( text = myName +"/"+ str(myID)+"/"+ str(ValveNumber)+" "+extra),
                                   template='plotly_dark'
                                    ),
                )
    else:
        fig = go.Figure(

                   data=[go.Bar(x=Time, y=Y, 
                                   #mode='markers',
				   marker={"line" : {"width" : 5, "color" : "red"}}
				   )], 
				   layout=go.Layout(
                                   title = go.layout.Title( text = myName +"/"+ str(myID)+"/"+ str(ValveNumber)+" "+extra),
                                   yaxis= go.layout.YAxis( range = (0,1)),
                                   template='plotly_dark'
                                    ),
		           ) 
    return fig

def returnaGraph(Valve, timeDelta):
    myName = getNameFromID(Valve['id'])  
    if (myName == "Inactive"):
        return html.Div(html.H5(children="Inactive/"+Valve["id"]+"/"+str(Valve["ValveNumber"]), style={'margin' : '10px'}))
        
    df = fetchCurrentValveData(Valve['id'], Valve["ValveNumber"], timeDelta)
    Graphs = []
    Internal = []
    Time = []
    Y = []
    for single in df:
    	Time.append(single[0])
    	Y.append(returnValveValue(single[1], Valve["ValveNumber"]))

    #print (Y)
    #print("YLen=",len(Y))
    if (True):
         extra = ""
         if (len(Y) == 0):
              Time = [1]
              Y = ["Off"]
              extra = "(No Valve Changes in Time Period)"
	
         fig = returnaFig(Valve['id'],Valve['ValveNumber'], Time, Y, extra)
         Graphs = dcc.Graph(
	 
         id = {'type' : 'VGdynamic', 'index': Valve["ValveNumber"]  , 'DeviceID' : Valve['id'] },
          config={'displayModeBar': False},
          animate=True,
	  responsive = True,

	  figure = fig,	
	            
          style={'height': 200},

             
	     )

    return html.Div(Graphs, style={'margin' : '10px'})

################
# Page Functions
################


def ValveGraphPage():
    Row1 = html.Div(
        [ 
            dbc.Row(
                [
		    dbc.Col(html.Div(fullDisplayGraphs()))
                ],
            ),
        ]
    )
    #layout = dbc.Container([
    #layout = dbc.Container([
    #    Row1],
    #    className="p-5",
    #)
    return Row1







