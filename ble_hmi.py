#-------------------------------------------------------------------------------
# Author:      Jamol Yunusov
#
# Created:     10/12/2022
# Copyright:   (c) Bridge Analyzers Inc 2022
#-------------------------------------------------------------------------------

#!/usr/bin/python3
from ble_logger import ADD_ALARM_ON1, ADD_ALARM_ON2, ADD_ALARM_ON3
from ble_logger import ADD_ALARM_OFF1, ADD_ALARM_OFF2, ADD_ALARM_OFF3
from ble_logger import SUB_ALARM_ON1, SUB_ALARM_ON2, SUB_ALARM_ON3
from ble_logger import SUB_ALARM_OFF1, SUB_ALARM_OFF2, SUB_ALARM_OFF3
from ble_logger import ADD_DELAY_TIMER1, ADD_DELAY_TIMER2, ADD_DELAY_TIMER3
from ble_logger import RESET_DELAY_TIMER1, RESET_DELAY_TIMER2, RESET_DELAY_TIMER3
from ble_logger import ENABLE_USER_CONF1, ENABLE_USER_CONF2, ENABLE_USER_CONF3
from ble_logger import ENABLE_RELAY1, ENABLE_RELAY2, ENABLE_RELAY3
from ble_logger import CONVERT_TO_KNOTS1, CONVERT_TO_KNOTS2, CONVERT_TO_KNOTS3
from ble_logger import CONVERT_TO_KPH1, CONVERT_TO_KPH2, CONVERT_TO_KPH3
from ble_logger import CONVERT_TO_MPH1, CONVERT_TO_MPH2, CONVERT_TO_MPH3
from ble_logger import CONVERT_TO_MS1, CONVERT_TO_MS2, CONVERT_TO_MS3
from ble_logger import WIFI_CONNECTION, NEW_WIFI_CONNECTION
from ble_logger import DISABLE_WIRED_ANEM, ENABLE_WIRED_ANEM
from ble_logger import log_process
from ble_logger import *
import serial
import threading
import asyncio
import sys


# Serial
ser = serial.Serial(
	port='/dev/ttyS0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=0.001)

ser.reset_input_buffer()
ser.reset_output_buffer()
ser.flushInput()
ser.flushOutput()


def NEXTION_DISPLAY_FUNCTION():

	ser.reset_input_buffer()
	ser.reset_output_buffer()
	ser.flushInput()
	ser.flushOutput()
	
	# Run while loop
	while True:
		try:
			output = ser.readline()
			if output:

				# Enable user config
				if output == b'e\x07\x04\x00\xff\xff\xff': # Enable / Disable user output 1
					ENABLE_USER_CONF1()
				
				if output == b'e\x07\x05\x00\xff\xff\xff': # Enable / Disable usre output 2
					ENABLE_USER_CONF2()
				
				if output == b'e\x07\x06\x00\xff\xff\xff': # Enable / Disable output 3
					ENABLE_USER_CONF3()


				# Alarm On
				if output == b'e\x0C\x0D\x00\xff\xff\xff': # Add alarm on - output 1
					ADD_ALARM_ON1()
				
				if output == b'e\x0D\x11\x00\xff\xff\xff': # Add alarm on - output 2
					ADD_ALARM_ON2()
				
				if output == b'e\x0E\x11\x00\xff\xff\xff': # Add alarm on - output 3
					ADD_ALARM_ON3()

				if output == b'e\x0C\x0E\x00\xff\xff\xff': # Decrease alarm on - output 1
					SUB_ALARM_ON1()

				if output == b'e\x0D\x12\x00\xff\xff\xff': # Decrease alarm on - output 2
					SUB_ALARM_ON2()

				if output == b'e\x0E\x12\x00\xff\xff\xff': # Decrease alarm on - output 3
					SUB_ALARM_ON3()


				# Alarm Off
				if output == b'e\x0C\x11\x00\xff\xff\xff': # Add alarm off - output 1
					ADD_ALARM_OFF1()
				
				if output == b'e\x0D\x13\x00\xff\xff\xff': # Add alarm off - output 2
					ADD_ALARM_OFF2()
				
				if output == b'e\x0E\x13\x00\xff\xff\xff': # Add alarm off - output 3
					ADD_ALARM_OFF3()
				
				if output == b'e\x0C\x12\x00\xff\xff\xff': # Decrease alarm off - output 1
					SUB_ALARM_OFF1()
				
				if output == b'e\x0D\x14\x00\xff\xff\xff': # Decrease alarm off - output 2
					SUB_ALARM_OFF2()
				
				if output == b'e\x0E\x14\x00\xff\xff\xff': # Decrease alarm off - output 3
					SUB_ALARM_OFF3()


				# Off Delay Timer
				if output == b'e\x0C\x13\x00\xff\xff\xff': # Add minutes - output 1
					ADD_DELAY_TIMER1()
				
				if output == b'e\x0D\x15\x00\xff\xff\xff': # Add minutes - output 2
					ADD_DELAY_TIMER2()
				
				if output == b'e\x0E\x15\x00\xff\xff\xff': # Add minutes - output 3
					ADD_DELAY_TIMER3()
				
				if output == b'e\x0C\x14\x00\xff\xff\xff': # Reset minutes - output 1
					RESET_DELAY_TIMER1()
				
				if output == b'e\x0D\x16\x00\xff\xff\xff': # Reset minutes - output 2
					RESET_DELAY_TIMER2()
				
				if output == b'e\x0E\x16\x00\xff\xff\xff': # Reset minutes - output 3
					RESET_DELAY_TIMER3()


				# Wind val conversion
				if output == b'e\x06\x01\x00\xff\xff\xff': # To mph
					CONVERT_TO_MPH1()
					CONVERT_TO_MPH2()
					CONVERT_TO_MPH3()

				if output == b'e\x06\x02\x00\xff\xff\xff': # To kph
					CONVERT_TO_KPH1()
					CONVERT_TO_KPH2()
					CONVERT_TO_KPH3()
				
				if output == b'e\x06\x03\x00\xff\xff\xff': # To knots
					CONVERT_TO_KNOTS1()
					CONVERT_TO_KNOTS2()
					CONVERT_TO_KNOTS3()

				if output == b'e\x06\x04\x00\xff\xff\xff': # To ms
					CONVERT_TO_MS1()
					CONVERT_TO_MS2()
					CONVERT_TO_MS3()


				# Controlling Relays
				if output == b'e\x0C\x07\x00\xff\xff\xff': # Enable / Disable relay 1
					ENABLE_RELAY1()
				
				if output == b'e\x0D\x09\x00\xff\xff\xff': # Enable / Disable relay 2
					ENABLE_RELAY2()
				
				if output == b'e\x0E\x09\x00\xff\xff\xff': # Enable / Disable relay 3
					ENABLE_RELAY3()


				# Check Wi-Fi connection
				if output == b'e\x08\x02\x00\xff\xff\xff':
					WIFI_CONNECTION()

				# New Wi-Fi connection
				if output == b'e\x09\x03\x00\xff\xff\xff':
					NEW_WIFI_CONNECTION()
				
				'''
				# Enable wired anemometer
				if output == b'e\x0B\x03\x00\xff\xff\xff':
					ENABLE_WIRED_ANEM()
				
				# Disable Wired anem
				if output == b'e\x0B\x01\x00\xff\xff\xff':
					DISABLE_WIRED_ANEM()
				'''
		except Exception:
			pass


# Threading
START_NEXTION = threading.Thread(target=NEXTION_DISPLAY_FUNCTION, daemon=True)
START_NEXTION.start()


if __name__ == "__main__":
    asyncio.run(log_process(sys.argv[1:]))
