#-------------------------------------------------------------------------------
# Author:      Jamol Yunusov
#
# Created:     10/12/2022
# Copyright:   (c) Bridge Analyzers Inc 2022
#-------------------------------------------------------------------------------

#!/usr/bin/python3
import os
from datetime import datetime
import time
import csv
import serial
import struct
import RPi.GPIO as GPIO
import threading
from ble_discover import *
from ble_discover import dir_raw_to_degrees, temp_raw_to_degrees_c, ws_raw_to_mph, ws_raw_to_kph, ws_raw_to_knots, ws_raw_to_ms, scan


# Serial connection
ser1 = serial.Serial(
	port='/dev/ttyS0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=0.1)

ser1.reset_input_buffer()
ser1.reset_output_buffer()
ser1.flushInput()
ser1.flushOutput()

# Converting data types into bytes
PACK_DATA = struct.pack('B', 0xff)

# Relay Channels
CH1 = 26 # Channel 1
CH2 = 20 # Channel 2
CH3 = 21 # Channel 3

# Setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CH1, GPIO.OUT)
GPIO.setup(CH2, GPIO.OUT)
GPIO.setup(CH3, GPIO.OUT)

# Turn off all Relays
GPIO.output(CH1, 1)
GPIO.output(CH2, 1)
GPIO.output(CH3, 1)

# Global wind variables
global WIND1_ALARM_ON_VAL
global WIND2_ALARM_ON_VAL
global WIND3_ALARM_ON_VAL
global WIND1_ALARM_OFF_VAL
global WIND2_ALARM_OFF_VAL
global WIND3_ALARM_OFF_VAL
global WIND1_OFF_DELAY_VAL
global WIND2_OFF_DELAY_VAL
global WIND3_OFF_DELAY_VAL

# Global min variables
global GET_MINS_WIND1
global GET_MINS_WIND2
global GET_MINS_WIND3
global SET_MINS_WIND1
global SET_MINS_WIND2
global SET_MINS_WIND3

# Setting default alarm-on value
WIND1_ALARM_ON_VAL = 0
WIND2_ALARM_ON_VAL = 0
WIND3_ALARM_ON_VAL = 0

# Setting default alarm-off value
WIND1_ALARM_OFF_VAL = 0
WIND2_ALARM_OFF_VAL = 0
WIND3_ALARM_OFF_VAL = 0

# Setting default off delay timer value
WIND1_OFF_DELAY_VAL = 0
WIND2_OFF_DELAY_VAL = 0
WIND3_OFF_DELAY_VAL = 0

# Setting default min value
GET_MINS_WIND1 = 0
GET_MINS_WIND2 = 0
GET_MINS_WIND3 = 0
SET_MINS_WIND1 = 0
SET_MINS_WIND2 = 0
SET_MINS_WIND3 = 0

# Button status
ENABLE_BTN1 = False
ENABLE_BTN2 = False
ENABLE_BTN3 = False

# Relay status
RELAY_1_STS = False
RELAY_2_STS = False
RELAY_3_STS = False

global ws_mph
ws_mph = 0
received_devices = []

# Passing string values
def GET_MPH(STRING):
	command_mph = 'mph.txt="' + STRING + '"'
	ser1.write(command_mph.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)

def GET_KPH(STRING):
	command_kph = 'kph.txt="' + STRING + '"'
	ser1.write(command_kph.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)

def GET_KNOT(STRING):
	command_knot = 'knot.txt="' + STRING + '"'
	ser1.write(command_knot.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)

def GET_MS(STRING):
	command_ms = 'ms.txt="' + STRING + '"'
	ser1.write(command_ms.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)

def GET_BT(STRING):
	ble_id = 'bt_id.txt="' + STRING + '"'
	ser1.write(ble_id.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)

def GET_RSSI(STRING):
	db = 'db.txt="' + STRING + '"'
	ser1.write(db.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)

def GET_TEMP(STRING):
	temp = 'temp.txt="' + STRING + '"'
	ser1.write(temp.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)

def ON_BUTTON(OBJ_NAME):
	command_on = OBJ_NAME + '.val=1'
	ser1.write(command_on.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)

def OFF_BUTTON(OBJ_NAME):
	command_off = OBJ_NAME + '.val=0'
	ser1.write(command_off.encode())
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)
	ser1.write(PACK_DATA)


# Wind val conversion
def CONVERT_TO_MPH1():
    global WIND1_ALARM_ON_VAL
    global ALARM_ON_VAL1
    global ALARM_OFF_VAL1

    alarm_on_mph = ALARM_ON_VAL1 * 0.6213711922
    ALARM_ON_VAL2 = round(alarm_on_mph)

    get_val = 'Wind1.alarm_on.val=' + str(ALARM_ON_VAL2)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_mph = ALARM_OFF_VAL1 * 0.6213711922
    ALARM_OFF_VAL2 = round(alarm_off_mph)

    get_valss = 'Wind1.alarm_off.val=' + str(ALARM_OFF_VAL2)
    ser1.write(get_valss.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    
    #print("MPH ON",ALARM_ON_VAL2,', MPH OFF', ALARM_OFF_VAL2)

def CONVERT_TO_MPH2():
    global WIND2_ALARM_ON_VAL

    alarm_on_mph = WIND2_ALARM_ON_VAL * 0.6213711922
    ALARM_ON_VAL = round(alarm_on_mph)

    get_val = 'Wind2.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_mph = WIND2_ALARM_OFF_VAL * 0.6213711922
    ALARM_OFF_VAL = round(alarm_off_mph)

    get_valss = 'Wind2.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_valss.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    
    #print("MPH ON",ALARM_ON_VAL,', MPH OFF', ALARM_OFF_VAL)

def CONVERT_TO_MPH3():
    global WIND3_ALARM_ON_VAL

    alarm_on_mph = WIND3_ALARM_ON_VAL * 0.6213711922
    ALARM_ON_VAL = round(alarm_on_mph)

    get_val = 'Wind3.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_mph = WIND3_ALARM_OFF_VAL * 0.6213711922
    ALARM_OFF_VAL = round(alarm_off_mph)

    get_valss = 'Wind3.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_valss.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    
    #print("MPH ON",ALARM_ON_VAL,', MPH OFF', ALARM_OFF_VAL)

def CONVERT_TO_KPH1():
    global WIND1_ALARM_ON_VAL
    global ALARM_ON_VAL1
    global ALARM_OFF_VAL1

    alarm_on_kph = WIND1_ALARM_ON_VAL * 1.60934
    ALARM_ON_VAL1 = round(alarm_on_kph)

    get_val = 'Wind1.alarm_on.val=' + str(ALARM_ON_VAL1)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_kph = WIND1_ALARM_OFF_VAL * 1.60934
    ALARM_OFF_VAL1 = round(alarm_off_kph)

    get_valss = 'Wind1.alarm_off.val=' + str(ALARM_OFF_VAL1)
    ser1.write(get_valss.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("KPH ON",ALARM_ON_VAL1,', KPH OFF', ALARM_OFF_VAL1)

def CONVERT_TO_KPH2():
    global WIND2_ALARM_ON_VAL

    alarm_on_kph = WIND2_ALARM_ON_VAL * 1.60934
    ALARM_ON_VAL = round(alarm_on_kph)

    get_val = 'Wind2.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_kph = WIND2_ALARM_OFF_VAL * 1.60934
    ALARM_OFF_VAL = round(alarm_off_kph)

    get_valss = 'Wind2.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_valss.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("KPH ON",ALARM_ON_VAL,', KPH OFF', ALARM_OFF_VAL)

def CONVERT_TO_KPH3():
    global WIND3_ALARM_ON_VAL

    alarm_on_kph = WIND3_ALARM_ON_VAL * 1.60934
    ALARM_ON_VAL = round(alarm_on_kph)

    get_val = 'Wind3.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_kph = WIND3_ALARM_OFF_VAL * 1.60934
    ALARM_OFF_VAL = round(alarm_off_kph)

    get_valss = 'Wind3.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_valss.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("KPH ON",ALARM_ON_VAL,', KPH OFF', ALARM_OFF_VAL)

def CONVERT_TO_KNOTS1():
    global WIND1_ALARM_ON_VAL

    alarm_on_knot = WIND1_ALARM_ON_VAL * 0.8689762419
    ALARM_ON_VAL = round(alarm_on_knot)

    get_val = 'Wind1.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_knot = WIND1_ALARM_OFF_VAL * 0.8689762419
    ALARM_OFF_VAL = round(alarm_off_knot)

    get_val = 'Wind1.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("KNOT ON",ALARM_ON_VAL,', KNOT OFF', ALARM_OFF_VAL)

def CONVERT_TO_KNOTS2():
    global WIND2_ALARM_ON_VAL

    alarm_on_knot = WIND2_ALARM_ON_VAL * 0.8689762419
    ALARM_ON_VAL = round(alarm_on_knot)

    get_val = 'Wind2.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_knot = WIND2_ALARM_OFF_VAL * 0.8689762419
    ALARM_OFF_VAL = round(alarm_off_knot)

    get_val = 'Wind2.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("KNOT ON",ALARM_ON_VAL,', KNOT OFF', ALARM_OFF_VAL)

def CONVERT_TO_KNOTS3():
    global WIND3_ALARM_ON_VAL

    alarm_on_knot = WIND3_ALARM_ON_VAL * 0.8689762419
    ALARM_ON_VAL = round(alarm_on_knot)

    get_val = 'Wind3.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_knot = WIND3_ALARM_OFF_VAL * 0.8689762419
    ALARM_OFF_VAL = round(alarm_off_knot)

    get_val = 'Wind3.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("KNOT ON",ALARM_ON_VAL,', KNOT OFF', ALARM_OFF_VAL)

def CONVERT_TO_MS1():
    global WIND1_ALARM_ON_VAL

    alarm_on_ms = WIND1_ALARM_ON_VAL * 0.44704
    ALARM_ON_VAL = round(alarm_on_ms)

    get_val = 'Wind1.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_ms = WIND1_ALARM_OFF_VAL * 0.44704
    ALARM_OFF_VAL = round(alarm_off_ms)

    get_val = 'Wind1.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("M/S ON",ALARM_ON_VAL,', M/S OFF', ALARM_OFF_VAL)

def CONVERT_TO_MS2():
    global WIND2_ALARM_ON_VAL

    alarm_on_ms = WIND2_ALARM_ON_VAL * 0.44704
    ALARM_ON_VAL = round(alarm_on_ms)

    get_val = 'Wind2.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_ms = WIND2_ALARM_OFF_VAL * 0.44704
    ALARM_OFF_VAL = round(alarm_off_ms)

    get_val = 'Wind2.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("M/S ON",ALARM_ON_VAL,', M/S OFF', ALARM_OFF_VAL)

def CONVERT_TO_MS3():
    global WIND3_ALARM_ON_VAL

    alarm_on_ms = WIND3_ALARM_ON_VAL * 0.44704
    ALARM_ON_VAL = round(alarm_on_ms)

    get_val = 'Wind3.alarm_on.val=' + str(ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    alarm_off_ms = WIND3_ALARM_OFF_VAL * 0.44704
    ALARM_OFF_VAL = round(alarm_off_ms)

    get_val = 'Wind3.alarm_off.val=' + str(ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    #print("M/S ON",ALARM_ON_VAL,', M/S OFF', ALARM_OFF_VAL)


# Status light
def STATUS_LIGHT_RED():
    command = 'output1.bco=63488'
    ser1.write(command.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    command = 'output2.bco=63488'
    ser1.write(command.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    command = 'output3.bco=63488'
    ser1.write(command.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def STATUS_LIGHT_GREEN():
    command = 'output1.bco=2016'
    ser1.write(command.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    command = 'output2.bco=2016'
    ser1.write(command.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    command = 'output3.bco=2016'
    ser1.write(command.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)


# Check Wi-Fi connection
def WIFI_CONNECTION():
    check_connection = os.popen("ping -c 1 google.com").read()
    wifi_id = os.popen('sudo iwgetid')

    for line in wifi_id:
        if "ESSID" in line:
            essid_name = line.split('ESSID:"', 1)[1].split('"', 1)[0]

    if check_connection == '':
        command = 'sts.txt="Not Connected"'
        ser1.write(command.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

        command = 'Wifi.p0.pic=7'
        ser1.write(command.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
    else:
        command = 'sts.txt="Connected"'
        ser1.write(command.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

        command = 'essid.txt="' + essid_name + '"'
        ser1.write(command.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

        command = 'Wifi.p0.pic=5'
        ser1.write(command.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

# New Wi-Fi connection
def NEW_WIFI_CONNECTION():
    command_name = 'name_txt.txt'
    ser1.write(command_name.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    command_pass = 'pass_txt.txt'
    ser1.write(command_pass.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    if command_pass == '':
        os.system('sudo iwconfig wlan0 essid ' + command_name)
    else:
        os.system('sudo iwconfig wlan0 essid ' + command_name + ' key s:' + command_pass)


# Enable wired anem
def ENABLE_WIRED_ANEM():
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(5, GPIO.FALLING)

# Disable wired anem
def DISABLE_WIRED_ANEM():
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(5, GPIO.RISING)


# User configs
def ENABLE_USER_CONF1():
    global WIND1_ALARM_ON_VAL
    global WIND1_ALARM_OFF_VAL
    global WIND1_OFF_DELAY_VAL
    global ENABLE_BTN1

    if ENABLE_BTN1 == False:
        ENABLE_BTN1 = True
        DEFAULT_VAL_WIND1()
    else:
        ENABLE_BTN1 = False
        WIND1_ALARM_ON_VAL = 0 
        WIND1_ALARM_OFF_VAL = 0
        WIND1_OFF_DELAY_VAL = 0

        get_vals = 'Wind1.alarm_on.val=' + str(WIND1_ALARM_ON_VAL)
        ser1.write(get_vals.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

        get_vals = 'Wind1.alarm_off.val=' + str(WIND1_ALARM_OFF_VAL)
        ser1.write(get_vals.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

def ENABLE_USER_CONF2():
    global WIND2_ALARM_ON_VAL
    global WIND2_ALARM_OFF_VAL
    global WIND2_OFF_DELAY_VAL
    global ENABLE_BTN2

    if ENABLE_BTN2 == False:
        ENABLE_BTN2 = True
        DEFAULT_VAL_WIND2()
    else:
        ENABLE_BTN2 = False
        WIND2_ALARM_ON_VAL = 0 
        WIND2_ALARM_OFF_VAL = 0
        WIND2_OFF_DELAY_VAL = 0

        get_vals = 'Wind2.alarm_on.val=' + str(WIND2_ALARM_ON_VAL)
        ser1.write(get_vals.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

        get_vals = 'Wind2.alarm_off.val=' + str(WIND2_ALARM_OFF_VAL)
        ser1.write(get_vals.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

def ENABLE_USER_CONF3():
    global WIND3_ALARM_ON_VAL
    global WIND3_ALARM_OFF_VAL
    global WIND3_OFF_DELAY_VAL
    global ENABLE_BTN3

    if ENABLE_BTN3 == False:
        ENABLE_BTN3 = True
        DEFAULT_VAL_WIND3()
    else:
        ENABLE_BTN3 = False
        WIND3_ALARM_ON_VAL = 0 
        WIND3_ALARM_OFF_VAL = 0
        WIND3_OFF_DELAY_VAL = 0

        get_vals = 'Wind3.alarm_on.val=' + str(WIND3_ALARM_ON_VAL)
        ser1.write(get_vals.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)

        get_vals = 'Wind3.alarm_off.val=' + str(WIND3_ALARM_OFF_VAL)
        ser1.write(get_vals.encode())
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)
        ser1.write(PACK_DATA)  


# Relays
def ENABLE_RELAY1():
    global RELAY_1_STS

    if RELAY_1_STS == False:
        GPIO.output(CH1, 0)
        RELAY_1_STS = True
        ON_BUTTON('manual1_btn')
    else:
        GPIO.output(CH1, 1)
        RELAY_1_STS = False
        OFF_BUTTON('manual1_btn')

def ENABLE_RELAY2():
    global RELAY_2_STS

    if RELAY_2_STS == False:
        GPIO.output(CH2, 0)
        RELAY_2_STS = True
        ON_BUTTON('manual2_btn')
    else:
        GPIO.output(CH2, 1)
        RELAY_2_STS = False
        OFF_BUTTON('manual2_btn')

def ENABLE_RELAY3():
    global RELAY_3_STS

    if RELAY_3_STS == False:
        GPIO.output(CH3, 0)
        RELAY_3_STS = True
        ON_BUTTON('manual3_btn')
    else:
        GPIO.output(CH3, 1)
        RELAY_3_STS = False
        OFF_BUTTON('manual3_btn')


# Default wind vals
def DEFAULT_VAL_WIND1():

    global WIND1_ALARM_ON_VAL
    global WIND1_ALARM_OFF_VAL
    global WIND1_OFF_DELAY_VAL

    WIND1_ALARM_ON_VAL = 8
    WIND1_ALARM_OFF_VAL = 6

    get_vals = 'Wind1.alarm_on.val=' + str(WIND1_ALARM_ON_VAL)
    ser1.write(get_vals.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    get_vals = 'Wind1.alarm_off.val=' + str(WIND1_ALARM_OFF_VAL)
    ser1.write(get_vals.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def DEFAULT_VAL_WIND2():

    global WIND2_ALARM_ON_VAL
    global WIND2_ALARM_OFF_VAL

    WIND2_ALARM_ON_VAL = 8
    WIND2_ALARM_OFF_VAL = 6

    get_vals1 = 'Wind2.alarm_on.val=' + str(WIND2_ALARM_ON_VAL)
    ser1.write(get_vals1.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    get_vals3 = 'Wind2.alarm_off.val=' + str(WIND2_ALARM_OFF_VAL)
    ser1.write(get_vals3.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def DEFAULT_VAL_WIND3():

    global WIND3_ALARM_ON_VAL
    global WIND3_ALARM_OFF_VAL

    WIND3_ALARM_ON_VAL = 8
    WIND3_ALARM_OFF_VAL = 6

    get_vals2 = 'Wind3.alarm_on.val=' + str(WIND3_ALARM_ON_VAL)
    ser1.write(get_vals2.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

    get_vals3 = 'Wind3.alarm_off.val=' + str(WIND3_ALARM_OFF_VAL)
    ser1.write(get_vals3.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)


# Alarm on
def ADD_ALARM_ON1():
    global WIND1_ALARM_ON_VAL
    WIND1_ALARM_ON_VAL += 1

    get_val = 'Wind1.alarm_on.val=' + str(WIND1_ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def ADD_ALARM_ON2():
    global WIND2_ALARM_ON_VAL
    WIND2_ALARM_ON_VAL += 1

    get_val = 'Wind2.alarm_on.val=' + str(WIND2_ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def ADD_ALARM_ON3():
    global WIND3_ALARM_ON_VAL
    WIND3_ALARM_ON_VAL += 1

    get_val = 'Wind3.alarm_on.val=' + str(WIND3_ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def SUB_ALARM_ON1():
    global WIND1_ALARM_ON_VAL
    WIND1_ALARM_ON_VAL -= 1

    get_val = 'Wind1.alarm_on.val=' + str(WIND1_ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def SUB_ALARM_ON2():
    global WIND2_ALARM_ON_VAL
    WIND2_ALARM_ON_VAL -= 1

    get_val = 'Wind2.alarm_on.val=' + str(WIND2_ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def SUB_ALARM_ON3():
    global WIND3_ALARM_ON_VAL
    WIND3_ALARM_ON_VAL -= 1

    get_val = 'Wind3.alarm_on.val=' + str(WIND3_ALARM_ON_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)


# Alarm off
def ADD_ALARM_OFF1():
    global WIND1_ALARM_OFF_VAL
    WIND1_ALARM_OFF_VAL += 1

    get_val = 'Wind1.alarm_off.val=' + str(WIND1_ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def ADD_ALARM_OFF2():
    global WIND2_ALARM_OFF_VAL
    WIND2_ALARM_OFF_VAL += 1

    get_val = 'Wind2.alarm_off.val=' + str(WIND2_ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def ADD_ALARM_OFF3():
    global WIND3_ALARM_OFF_VAL
    WIND3_ALARM_OFF_VAL += 1

    get_val = 'Wind3.alarm_off.val=' + str(WIND3_ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def SUB_ALARM_OFF1():
    global WIND1_ALARM_OFF_VAL
    WIND1_ALARM_OFF_VAL -= 1

    get_val = 'Wind1.alarm_off.val=' + str(WIND1_ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def SUB_ALARM_OFF2():
    global WIND2_ALARM_OFF_VAL
    WIND2_ALARM_OFF_VAL -= 1

    get_val = 'Wind2.alarm_off.val=' + str(WIND2_ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def SUB_ALARM_OFF3():
    global WIND3_ALARM_OFF_VAL
    WIND3_ALARM_OFF_VAL -= 1

    get_val = 'Wind3.alarm_off.val=' + str(WIND3_ALARM_OFF_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)


# Add delay timer
def ADD_DELAY_TIMER1():
    global WIND1_OFF_DELAY_VAL
    global GET_MINS_WIND1
    global SET_MINS_WIND1

    WIND1_OFF_DELAY_VAL += 1
    GET_MINS_WIND1 = 60
    GET_MINS_WIND1 *= WIND1_OFF_DELAY_VAL
    SET_MINS_WIND1 = GET_MINS_WIND1

    get_val = 'Wind1.delay_timer.val=' + str(WIND1_OFF_DELAY_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def ADD_DELAY_TIMER2():
    global WIND2_OFF_DELAY_VAL
    global GET_MINS_WIND2
    global SET_MINS_WIND2

    WIND2_OFF_DELAY_VAL += 1
    GET_MINS_WIND2 = 60
    GET_MINS_WIND2 *= WIND2_OFF_DELAY_VAL
    SET_MINS_WIND2 = GET_MINS_WIND2

    get_val = 'Wind2.delay_timer.val=' + str(WIND2_OFF_DELAY_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def ADD_DELAY_TIMER3():
    global WIND3_OFF_DELAY_VAL
    global GET_MINS_WIND3
    global SET_MINS_WIND3

    WIND3_OFF_DELAY_VAL += 1
    GET_MINS_WIND3 = 60
    GET_MINS_WIND3 *= WIND3_OFF_DELAY_VAL
    SET_MINS_WIND3 = GET_MINS_WIND3

    get_val = 'Wind3.delay_timer.val=' + str(WIND3_OFF_DELAY_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)


# Reset delay timer
def RESET_DELAY_TIMER1():
    global WIND1_OFF_DELAY_VAL
    global GET_MINS_WIND1
    global SET_MINS_WIND1

    WIND1_OFF_DELAY_VAL = 0
    GET_MINS_WIND1 = 0
    SET_MINS_WIND1 = GET_MINS_WIND1

    get_val = 'Wind1.delay_timer.val=' + str(WIND1_OFF_DELAY_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def RESET_DELAY_TIMER2():
    global WIND2_OFF_DELAY_VAL
    global GET_MINS_WIND2
    global SET_MINS_WIND2

    WIND2_OFF_DELAY_VAL = 0
    GET_MINS_WIND2 = 0
    SET_MINS_WIND2 = GET_MINS_WIND2

    get_val = 'Wind2.delay_timer.val=' + str(WIND2_OFF_DELAY_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)

def RESET_DELAY_TIMER3():
    global WIND3_OFF_DELAY_VAL
    global GET_MINS_WIND3
    global SET_MINS_WIND3
    
    WIND3_OFF_DELAY_VAL = 0
    GET_MINS_WIND3 = 0
    SET_MINS_WIND3 = GET_MINS_WIND3

    get_val = 'Wind3.delay_timer.val=' + str(WIND3_OFF_DELAY_VAL)
    ser1.write(get_val.encode())
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)
    ser1.write(PACK_DATA)


# Start delay timer
def OFF_DELAY_TIMER_WIND1():
    global SET_MINS_WIND1

    while SET_MINS_WIND1:
        mins, secs = divmod(SET_MINS_WIND1, 60)
        timeformat1 = '{:02d}:{:02d}'.format(mins, secs)
        #print('wind1 ', timeformat1, end='\r')
        SET_MINS_WIND1 -= 1
        
        if SET_MINS_WIND1 == 0:
            GPIO.output(CH1, 1)
            OFF_BUTTON('manual1_btn')
        else:
            pass
        break

def OFF_DELAY_TIMER_WIND2():
    global SET_MINS_WIND2

    while SET_MINS_WIND2:
        mins, secs = divmod(SET_MINS_WIND2, 60)
        timeformat2 = '{:02d}:{:02d}'.format(mins, secs)
        #print('wind2 ', timeformat2, end='\r')
        SET_MINS_WIND2 -= 1
        
        if SET_MINS_WIND2 == 0:
            GPIO.output(CH2, 1)
            OFF_BUTTON('manual2_btn')
        else:
            pass
        break

def OFF_DELAY_TIMER_WIND3():
    global SET_MINS_WIND3

    while SET_MINS_WIND3:
        mins, secs = divmod(SET_MINS_WIND3, 60)
        timeformat3 = '{:02d}:{:02d}'.format(mins, secs)
        #print('wind3 ', timeformat3, end='\r')
        SET_MINS_WIND3 -= 1
        
        if SET_MINS_WIND3 == 0:
            GPIO.output(CH3, 1)
            OFF_BUTTON('manual3_btn')
        else:
            pass
        break


# Loop outputs
def START_LOOP_WIND1():
    global SET_MINS_WIND1
    global GET_MINS_WIND1
    global ws_mph

    if WIND1_ALARM_ON_VAL or WIND1_ALARM_OFF_VAL > 0:
        if int(ws_mph) >= int(WIND1_ALARM_ON_VAL):
            GPIO.output(CH1, 0)
            ON_BUTTON('manual1_btn')
            SET_MINS_WIND1 = GET_MINS_WIND1
            STATUS_LIGHT_RED()
        elif int(ws_mph) < int(WIND1_ALARM_OFF_VAL):
            if SET_MINS_WIND1 > 0:
                OFF_DELAY_TIMER_WIND1()
            else:
                GPIO.output(CH1, 1)
                OFF_BUTTON('manual1_btn')
            STATUS_LIGHT_GREEN()

def START_LOOP_WIND2():
    global SET_MINS_WIND2
    global GET_MINS_WIND2
    global ws_mph
    
    if WIND2_ALARM_ON_VAL or WIND2_ALARM_OFF_VAL > 0:
        if int(ws_mph) >= int(WIND2_ALARM_ON_VAL):
            GPIO.output(CH2, 0)
            ON_BUTTON('manual2_btn')
            SET_MINS_WIND2 = GET_MINS_WIND2
        elif int(ws_mph) < int(WIND2_ALARM_OFF_VAL):
            if SET_MINS_WIND2 > 0:
                OFF_DELAY_TIMER_WIND2()
            else:
                GPIO.output(CH2, 1)
                OFF_BUTTON('manual2_btn')

def START_LOOP_WIND3():
    global SET_MINS_WIND3
    global GET_MINS_WIND3
    global ws_mph
    
    if WIND3_ALARM_ON_VAL or WIND3_ALARM_OFF_VAL > 0:
        if int(ws_mph) >= int(WIND3_ALARM_ON_VAL):
            GPIO.output(CH3, 0)
            ON_BUTTON('manual3_btn')
            SET_MINS_WIND3 = GET_MINS_WIND3
        elif int(ws_mph) < int(WIND3_ALARM_OFF_VAL):
            if SET_MINS_WIND3 > 0:
                OFF_DELAY_TIMER_WIND3()
            else:
                GPIO.output(CH3, 1)
                OFF_BUTTON('manual3_btn')


# Wind sensor data can be filtered based on sensor id
# If no ids are provided, all sensor data will be recorded
async def log_process(ids = []):

    global ws_mph
    global ws_kph
    global ws_knots
    global ws_ms
    
    ids = [int(i, 16) for i in ids]

    # Create log directory
    dir_name = "wind logs"
    try:
        os.mkdir(dir_name)
    except:
        pass  # directory already exists

    # Create new log file with date and time
    date = datetime.now().strftime("%Y-%m-%d-%H-%M")
    f = open(f"{dir_name}/log_{date}.csv", mode="w")
    writer = csv.writer(f, delimiter=",")

    # Create csv file header
    # print(f"Time, Device, RSSI, Wind Speed, Wind Direction, Temperature")
    writer.writerow([f'Time ', f'Device ', f'dB', f'Wind Speed ', f'Wind Direction ', f'Temperature '])

    # Scan for devices
    while True:
        try:
            # Scan for wind sensors every 1 seconds
            ble_data = await scan(1)
            for device_id, device_data in ble_data.items():
                if not ids or device_id in ids:

                    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
                    temp_f = temp_raw_to_degrees_c(ble_data[device_id]["temp"])
                    ws_mph = ws_raw_to_mph(ble_data[device_id]["wind_speed"])
                    ws_kph = ws_raw_to_kph(ble_data[device_id]["wind_speed"])
                    ws_knots = ws_raw_to_knots(ble_data[device_id]["wind_speed"])
                    ws_ms = ws_raw_to_ms(ble_data[device_id]["wind_speed"])
                    direction = dir_raw_to_degrees(ble_data[device_id]["wind_dir"])

                    if ws_mph == 0:
                        GET_KNOT(str('- -'))
                        GET_MPH(str('- -'))
                        GET_KPH(str('- -'))
                        GET_MS(str('- -'))
                    else:
                        GET_MPH(str(ws_mph))
                        GET_KNOT(str(ws_knots))
                        GET_KPH(str(ws_kph))
                        GET_MS(str(ws_ms))
                    
                    GET_BT(str(f'{device_id:x}'))
                    GET_TEMP(str(f'{temp_f:.1f} C'))
                    GET_RSSI(str(ble_data[device_id]["rssi"]))

                    # print(f'{date_time},{device_id:x},{ble_data[device_id]["rssi"]},{ws_mph:.2f},{direction:.2f},{temp_f:.2f}')
                    writer.writerow(
                        [f'{date_time}',
                        f'{device_id:x}',
                        f'{ble_data[device_id]["rssi"]}',
                        f'{ws_mph:.2f}',
                        f'{direction:.2f}',
                        f'{temp_f:.2f}'])
        except:pass

        START_LOOP_WIND1()
        START_LOOP_WIND2()
        START_LOOP_WIND3()

#if __name__ == "__main__":
   #asyncio.run(log_process(sys.argv[1:]))