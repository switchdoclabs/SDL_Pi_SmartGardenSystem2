import os
import shutil
import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, MATCH, ALL, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import traceback
import datetime

import time

import moisture_sensors 
import status_page 
import valve_graphs
import log_page
import weather_page

from non_impl import NotImplPage 

from navbar import Navbar, Logo
logo = Logo()
print("new navbar=")
nav = Navbar()

#nav = html.Div([dcc.Link('Weather Page', href='/weather_page'),
#    html.Br(),
#    dcc.Link('status page', href='/status_page'), 
#    ])

newValveState = ""
# state of previous page
previousPathname = ""

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE])

app.config.suppress_callback_exceptions = True


app.layout =  html.Div(

        [

       html.Div(id='my-output-interval'),

       dcc.Interval(
            id='main-interval-component',
            interval=10*1000, # in milliseconds - leave as 10 seconds
            n_intervals=0
            ) ,
       #dcc.Interval(
       #     id='weather-update-interval-component',
       #     interval=5*1000, # in milliseconds
       #     n_intervals=0
       #     ) ,
       
        #dbc.Spinner(id="main-spinner", color="white" ),
        #dcc.Location(id = 'url', refresh = True),
        dcc.Location(id = 'url', refresh = False),

        html.Div(id = 'page-content'),
        #html.Div(id = 'wp-placeholder', style={'display':'none'}) 
        ],

        id="mainpage"

    )
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])


def display_page(pathname):
    global previousPathname

    print("--------------------->>>>>>>>>>>>>>>>new page")
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    print("begin=",nowString)
    
    print("pathname=", pathname)
    print("previousPathname=", previousPathname)
    i = [i['prop_id'] for i in dash.callback_context.triggered]
    print('i=', i)
    print('TRIGGER(S):', [i['prop_id'] for i in dash.callback_context.triggered])
    if (i[0] == '.'):
        print("---no page change--- ['.']")
        raise PreventUpdate	
    #if (pathname == previousPathname):
    #    print("---no page change---Equal Pathname")
    #    raise PreventUpdate	
    previousPathname = pathname
    
    myLayout = NotImplPage()
    myLayout2 = ""
    if pathname == '/status_page':
        myLayout = status_page.StatusPage() 
        myLayout2 = moisture_sensors.MoistureSensorPage()
    if pathname == '/valve_graphs':
        myLayout = valve_graphs.ValveGraphPage()
        myLayout2 = ""
    if pathname == '/log_page':
        myLayout = log_page.LogPage()
        myLayout2 = ""
    if pathname == '/weather_page':
        myLayout = weather_page.WeatherPage()
        myLayout2 = ""
    
    #print("myLayout= ",myLayout)
    #print("myLayout2= ",myLayout2)
    print("page-content= ",app.layout)
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    print("end=",nowString)
    return (logo, nav,myLayout, myLayout2 )

'''
@app.callback(
    Output("main-spinner", "children"), [Input("url", "pathname")]
)

def input_triggers_spinner(pathname):
    print("spinner=", pathname)

    if pathname == '/moisture_sensors':
        time.sleep(moisture_sensors.returnNumberTanksGraphs())
    else:
        time.sleep(1)
    return pathname 
'''
##################
# Moisture Sensors 
##################



@app.callback(Output({'type' : 'MSGdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'MSNumber' : MATCH, 'DeviceName' : MATCH, 'ValveNumber': MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'MSGdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'MSNumber' : MATCH, 'DeviceName' : MATCH, 'ValveNumber': MATCH}, 'id' )],
              [State({'type' : 'MSGdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'MSNumber' : MATCH, 'DeviceName' : MATCH, 'ValveNumber': MATCH}, 'value'  )]
              )


def update_moisturegraphs(n_intervals, id, value ):
    print("MS-n_intervals=", n_intervals)
    #if (True): # 5 minutes -10 second timer
    if ((n_intervals % (5*6)) == 0): # 5 minutes -10 second timer
 
        print(">moisture_sensors Graph Update started",id['index'], id['DeviceID'])
        #print("id=", id)
        #print ('Graph id {} / n_intervals = {}'.format(id['index'], n_intervals))
        myNewChart = moisture_sensors.updateGraph(id)
    
        fig = go.Figure(
            data=[go.Scatter(x=myNewChart[0], y=myNewChart[1])], layout=go.Layout(
                title = go.layout.Title( text = id['DeviceName'] +"/"+ str(id["DeviceID"])+"/"+ str(id["ValveNumber"])),
                yaxis= go.layout.YAxis( range = (0,101)),
                height= 300),
                        )
                     
    
        print("<moisture_sensors Graph Update complete",id['index'], id['DeviceID'])
        return fig 
    else:
        raise PreventUpdate

##################
# Log Page 
##################
@app.callback(Output({'type' : 'LPdynamic', 'index' : MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'LPdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'LPdynamic', 'index' : MATCH}, 'value'  )]
              )

def logpageupdate(n_intervals, id, value):
    
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
    print(">log_page table Update started",id['index'])
    print("LG-n_intervals=", n_intervals) 
    if (id['index'] == "systemlog"):
        data = log_page.fetchSystemLog()
        fig = log_page.buildTableFig(data,"System Log")
    
    if (id['index'] == "sensorlog"):
        data = log_page.fetchSensorLog()
        fig = log_page.buildTableFig(data,"Sensor Log")

    if (id['index'] == "valvelog"):
        data = log_page.fetchValveLog()
        fig = log_page.buildTableFig(data,"Valve Log")
        return fig
    
    print("<log_page table Update complete",id['index'])
    return fig
   else:
    raise PreventUpdate
##################
# Valve Graphs Page 
##################


@app.callback(Output({'type' : 'VGdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'VGdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'id' )],
              [State({'type' : 'VGdynamic', 'index' : MATCH, 'DeviceID' : MATCH, }, 'value'  )]
              )


def update_valve_graphs(n_intervals, id, value ):
 
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
    print(">valve_graphs Graph Update started",id['index'], id['DeviceID'])
    #print("id=", id)
    print("VG-n_intervals=", n_intervals)

    timeDelta = datetime.timedelta(days = 1) 
    df = valve_graphs.fetchCurrentValveData(id['DeviceID'], id["index"], timeDelta)
    myName = valve_graphs.getNameFromID(id['DeviceID'])  
    Graphs = []
    Internal = []
    Time = []
    Y = []
    for single in df:
    	Time.append(single[0])
    	Y.append(valve_graphs.returnValveValue(single[1], id["index"]))

    extra = ""
    if (len(Y) == 0):
        Time = [1]
        Y = ["Off"]
        extra = "(No Valve Changes in Time Period)"
	
    fig = valve_graphs.returnaFig(id['DeviceID'],id['index'], Time, Y, extra)

                    

    print("<valve_graphs Graph Update complete",id['index'], id['DeviceID'])

    return fig 
   else:
    raise PreventUpdate


##################
# Status Page
##################

@app.callback(
	      [
	      Output({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'value' ),
	      Output({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'label' )
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'id' )],
              [State({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'value'  )]
              )

def update_gauges(n_intervals, id, value):
   if (True): # 1 minutes -10 second timer
   #if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
     #print(">status_page Gauge Update started",id['GaugeType'])
     newValue = status_page.updateGauges(id) 
     if (id['GaugeType'] == 'pi-disk'):
        myName = "Pi SD Card Free" 
     if (id['GaugeType'] == 'pi-memory'):
        myName = "Pi Memory Usage" 
     if (id['GaugeType'] == 'pi-loading'):
        myName = "Pi CPU Loading" 
     #print("<status_page Gauge Update complete",id['GaugeType'])

     return newValue, myName 
   else:
    raise PreventUpdate


@app.callback(Output({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'id' )],
              [State({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color'  )]
              )

def update_statuspage(n_intervals, id, color):
   global newValveState
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
    #print(">status_page Indicator Update started",id['index'], id['DeviceID'])
    #print("id=", id)
    #print("newValveState=", newValveState)
    #print("n_intervals=", n_intervals)
    #print ('Indicator id {} / n_intervals = {}'.format(id['index'], n_intervals))
    if (newValveState == ""):
        newValveState = status_page.returnLatestValveRecord(id['DeviceID'] )

    status  = status_page.returnIndicatorValue(newValveState, id['index'])
    color = status_page.updateIndicator(status)

    if (id['index'] == 7):
        newValveState = ""    
    #print("<status_page Indicator Update complete",id['index'], id['DeviceID'])
    return color
   else:
    raise PreventUpdate

 
##################
# Weather Page
##################




#################
# Callbacks
#################
@app.callback(
	      [
	      Output({'type' : 'WPIdynamic', 'index' : 'SkyCamImage'}, 'children' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPIdynamic', 'index' : 'SkyCamImage'}, 'id' )],
              [State({'type' : 'WPIdynamic', 'index' : 'SkyCamImage'}, 'value'  )]
              )

def updateWeatherImagePage(n_intervals,id, value):
    print("updateWImageP n_intervals", n_intervals)
    if ((n_intervals % (1*6)) == 0) or (n_intervals ==0): # 1 minutes -10 second timer
        print("--->>>updateSkyCamImage", datetime.datetime.now(), n_intervals)
        try:
            # delete old file names

            fileList = glob.glob("/home/pi/SDL_Pi_SmartGardenSystem2/dash_app/assets/imagedisplay*")
            # Iterate over the list of filepaths & remove each file.
            for filePath in fileList:
                    os.remove(filePath)
                        
            # build names
            basename = "imagedisplay"+str(n_intervals)+".jpg"
            htmlname =  "/assets/"+ basename
            newname = "/home/pi/SDL_Pi_SmartGardenSystem2/dash_app/assets/"+basename 
        
            # move camera file to new name
            shutil.copy('/home/pi/SDL_Pi_SmartGardenSystem2/dash_app/assets/skycamera.jpg', newname)
            
            value = html.Div( [
                          html.Img( height=350, width=350*1.77, src=htmlname),             
                          html.Figcaption("Smart Garden Cam"),
                          ])


        except:
            print(traceback.format_exc())
            print("camera file not found")
            htmlname = "/assets/SGTextcolor.png"
            value = html.Div( [
                          html.Img( height=150, width=150*2.86, src=htmlname),             
                          html.Figcaption("Smart Garden Cam"),
                          ])

            pass
  
    else:
        raise PreventUpdate
    return [value]

@app.callback(
	      [
	      Output({'type' : 'WPdynamic', 'index' : MATCH}, 'children' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'WPdynamic', 'index' : MATCH}, 'value'  )]
              )

def updateWeatherTextPage(n_intervals,id, value):
    if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        CWJSON = weather_page.generateCurrerntWeatherJSON()
        #print(CWJSON)
        print("--->>>updateWeatherTextPage", datetime.datetime.now(), n_intervals)
        print("updateWTP n_intervals", n_intervals)
        value = str(CWJSON[id['index']]) +" "+ CWJSON[id['index']+'Units']
        if (id['index'] == "StringTime"):
            value = "Weather Instruments Updated at: "+value
    else:
        raise PreventUpdate
    return [value]


@app.callback(
	      [
	      Output({'type' : 'WPRdynamic', 'index' : MATCH}, 'figure' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPRdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'WPRdynamic', 'index' : MATCH}, 'value'  )]
              )

def updateWeatherRosePage(n_intervals,id, value):

    if (n_intervals == 0): # stop first update
        raise PreventUpdate
    print("WeatherRose n_intervals=", n_intervals)
    # update every 15 minutes
    #if (True): # 15 minutes -10 second timer
    if ((n_intervals % (15*6)) == 0): # 15 minutes -10 second timer
        print("--->>>updateCompassRose", datetime.datetime.now(), n_intervals)
        timeDelta = datetime.timedelta(days=7)
        data = weather_page.fetchWindData(timeDelta)
        fig = weather_page.figCompassRose(data)
 
    else:
        raise PreventUpdate
    return [fig]


@app.callback(
	      [
	      Output({'type' : 'WPGdynamic', 'index' : MATCH}, 'figure' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPGdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'WPGdynamic', 'index' : MATCH}, 'value'  )]
              )

def updateWeatherGraphPage(n_intervals,id, value):

    if (n_intervals == 0): # stop first update
        raise PreventUpdate

    #if (True): # 5 minutes -10 second timer
    if ((n_intervals % (5*6)) == 0): # 15 minutes -10 second timer
       print("--->>>updateWeatherGraphs", datetime.datetime.now(), n_intervals, id)
       if (id['index'] ==  'graph-oth'):
           fig = weather_page.buildOutdoorTemperature_Humidity_Graph_Figure()
       if (id['index'] ==  'graph-suv'):
           fig = weather_page.buildSunlightUVIndexGraphFigure()

    else:
        raise PreventUpdate
    return [fig]

##########################

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
