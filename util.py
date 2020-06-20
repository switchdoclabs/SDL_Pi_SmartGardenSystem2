#utility programs
import state
import config
################
# Unit Conversion
################
# 

def returnTemperatureCF(temperature):
	if (config.English_Metric == True):
		# return Metric 
		return temperature
	else:
		return (9.0/5.0)*temperature + 32.0

def returnTemperatureCFUnit():
	if (config.English_Metric == True):
		# return Metric 
		return "C"
	else:
		return  "F"



################
# Unit Conversion
################
# 

def returnTemperatureCF(temperature):
	if (config.English_Metric == True):
		# return Metric 
		return temperature
	else:
		return (9.0/5.0)*temperature + 32.0

def returnTemperatureCFUnit():
	if (config.English_Metric == True):
		# return Metric 
		return "C"
	else:
		return  "F"

def returnWindSpeedUnit():
	if (config.English_Metric == True):
		# return Metric 
		return "KPH"
	else:
		return  "MPH"

def returnWindSpeed(wind):
	if (config.English_Metric == True):
		# return Metric 
		return wind
	else:
		return wind/1.6


def returnWindDirection(windDirection):

    if (windDirection > 315.0+1.0):
        return "NNW"
    if (windDirection > 292.5+1.0):
        return "NW"
    if (windDirection > 270.0+1.0):
        return "WNW"
    if (windDirection > 247.5+1.0):
        return "W"
    if (windDirection > 225.0+1.0):
        return "WSW"
    if (windDirection > 202.5+1.0):
        return "SW"
    if (windDirection > 180.0+1.0):
        return "SSW"
    if (windDirection > 157.5+1.0):
        return "S"
    if (windDirection > 135.0+1.0):
        return "SSE"
    if (windDirection > 112.5+1.0):
        return "SE"
    if (windDirection > 90.0+1.0):
        return "ESE"
    if (windDirection > 67.5+1.0):
        return "E"
    if (windDirection > 45.0+1.0):
        return "ENE"
    if (windDirection > 22.5+1.0):
        return "NE"
    if (windDirection > 0.0+1.0):
        return "NNE"
    return "N"



