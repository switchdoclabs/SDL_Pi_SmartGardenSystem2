#!/usr/bin/env python

# Modified by SwtichDoc Labs July 2017

"""
 * ultrasonic.py
 * A library for ultrasonic sensor at RP
 *
 * Copyright (c) 2012 seeed technology inc.
 * Website    : www.seeed.cc
 * Author     : seeed fellow
 * Create Time:
 * Change Log :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
"""
from __future__ import division
from __future__ import print_function
from builtins import range
from past.utils import old_div
import RPi.GPIO as GPIO
import time

import config
import state

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def getAndPrint():

    print("Grove Ultrasonic get level and print")

    # test 10 times
    for i in range(10):
        print("%5.3fcm" % measurementInCM())
    # Reset GPIO settings
    #GPIO.cleanup()


def measurementInCM():

    # setup the GPIO_SIG as output
    GPIO.setup(config.UltrasonicLevel, GPIO.OUT)

    GPIO.output(config.UltrasonicLevel, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(config.UltrasonicLevel, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(config.UltrasonicLevel, GPIO.LOW)
    # initialize times for abort check
    start = -1
    stop = -1

    # setup GPIO_SIG as input
    GPIO.setup(config.UltrasonicLevel, GPIO.IN)

    measurementStartTime = time.time()
    # get duration from Ultrasonic SIG pin
    while GPIO.input(config.UltrasonicLevel) == 0:
        start = time.time()
        if (measurementStartTime+2<start):
            # abort
            return -1
    
    if (start == -1):
        # abort
        return -1

    measurementStartTime = time.time()
    while GPIO.input(config.UltrasonicLevel) == 1:
        stop = time.time()
        if (measurementStartTime+2<stop):
            # abort
            return -1

    if (stop == -1):
        # abort
        return -1

    pulseLength = measurementPulse(start, stop)

    return pulseLength


def measurementPulse(start, stop):


    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = old_div(distance, 2)

    return distance 

def readCalibrationNumbers():

    f = open("TankCalibration","r")

    line = f.read()
    line = line.strip()
    empty, full = line.split(",")
    state.Tank_Empty_Level = float(empty)
    state.Tank_Full_Level = float(full)
    f.close()

def returnPercentFull():
    measurement = measurementInCM()

    #check for abort
    if (measurement < 0.0):
        return -1.00
    state.Tank_Level = measurement
    
    
    full = (old_div((state.Tank_Empty_Level - state.Tank_Level),(state.Tank_Empty_Level - state.Tank_Full_Level)))*100.0


    if (config.SWDEBUG):
        print("returnPercentFull")
        print("state.Tank_Level:", state.Tank_Level)
        print("state.Tank_Empty_Level:", state.Tank_Empty_Level)
        print("state.Tank_Full_Level:", state.Tank_Full_Level)
        print("Old Tank_Percentage_Full= %f" % state.Tank_Percentage_Full)
        print("New Tank_Percentage_Full= %f" % full)

    if (full < 0.0):
        full = 0.0
    if (full > 100.0):
        full = 100.0
    if (config.SWDEBUG):
        print("Adjusted Tank_Percentage_Full= %f" % full)

    return full

