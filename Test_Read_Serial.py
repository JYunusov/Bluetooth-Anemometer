import serial 
import time 

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate =9600,           
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)

time.sleep(1) 
while True: 
	try:
		output = ser.readline()
		if output:
			print(output)
		time.sleep(0.5)

	except Exception:
		pass