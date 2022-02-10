import threading 
import time 
import os 
import sys
import serial

PORT = '/dev/ttyS0'
BAUDCOMM = 9600
BAUDUPLOAD = 115200

if len(sys.argv) != 2:
	print('usage: python %s file_to_upload.tft' % sys.argv[0])
	exit(-2)

file_path = sys.argv[1]

if os.path.isfile(file_path):
	print('uploading %s (%i bytes)...' % (file_path, os.path.getsize(file_path)))
else:
	print('file not found')
	exit(-1)

fsize = os.path.getsize(file_path)


ser = serial.Serial(PORT, BAUDCOMM, timeout=.1, )

waiting = False

def reader():
	global waiting
	while True:
		r = ser.read(128)
		if r == '': continue
		if waiting and '\x05' in r:
			waiting = False
			continue
		print('<%r>' % r)

threader = threading.Thread(target = reader)
threader.daemon = True
threader.start()

ser.write([0xff, 0xff, 0xff])
ser.write('connect')
ser.write([0xff, 0xff, 0xff])
time.sleep(.5)

ser.write('whmi-wri %i,%i,res0' % (fsize, BAUDUPLOAD))
ser.write([0xff, 0xff, 0xff])
time.sleep(.1)

waiting = True
ser.baudrate = BAUDUPLOAD
print('waiting hmi')
while waiting:
	pass

with open(file_path, 'rb') as hmif:
	dcount = 0
	while True:
		time.sleep(.1)
		data = hmif.read(4096)
		if len(data) == 0: break
		dcount += len(data)
		print('writing %i...' % len(data))
		ser.write(data)
		sys.stdout.write('\rDownloading, %3.3f...        ' % (dcount/868631.0*100.0))
		sys.stdout.flush()
		waiting = True
		print('waiting for hmi...')
		while waiting:
			pass


ser.close()