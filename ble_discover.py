#!/usr/bin/python3
import asyncio
from logging import exception

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


ETESIAN_COMPANY_ID = 0x0341

scanning = asyncio.Event()


# Complete one scan for a given duration
async def scan(duration):

    devices = await BleakScanner.discover(duration)
    recieved_data = dict()
    
    for device in devices:
        for key, value in device.metadata['manufacturer_data'].items():
            if key == ETESIAN_COMPANY_ID:
                device_id = int.from_bytes(value[2:4], 'big')
                recieved_data[device_id] = dict()
                recieved_data[device_id]['rssi'] = device.rssi
                recieved_data[device_id]['temp'] = int.from_bytes(value[0:1], 'big')
                recieved_data[device_id]['wind_speed'] = int.from_bytes(value[1:2], 'big')
                recieved_data[device_id]['wind_dir'] = int.from_bytes(value[4:5], 'big')

                # Alternative method of unpacking
                # values = struct.unpack('>BBhB', b'\xa010Y\x80')
                # recieved_data['wind_speed'] = values[1]
                # recieved_data['device_id'] = values[2]
                # recieved_data['temp'] = values[3]
                
                # print(f'{device.address}    RSSI: {device.rssi}, Wind Speed: {recieved_data[device_id]["wind_speed"]:#x}, Sensor ID: {device_id:#x}, Temperature: {recieved_data[device_id]["temp"]:#x}')

    return recieved_data


def ws_raw_to_mph(ws_raw):
    global ws

    if ws_raw == 0:
        ws_mph = 0
    else:
        ws_mph = 0.3874 * ws_raw + 2.34
    ws = int(ws_mph)
    return int(ws_mph)

def ws_raw_to_kph(ws_raw):
    ws_kph = .621371 * ws_raw + 2.34
    return int(ws_kph)

def ws_raw_to_knots(ws_raw):
    ws_knots = ws  * 0.868976
    return int(ws_knots)

def ws_raw_to_ms(ws_raw):
    ws_ms = ws * 0.44704
    return int(ws_ms)


def temp_raw_to_degrees_c(temp_raw):
    volts = 1.2 * temp_raw / 255
    temp_degrees_c = 100 * volts - 50
    return int(temp_degrees_c)

def temp_raw_to_degrees_f(temp_raw):
    volts = 1.2 * temp_raw / 255
    temp_degrees_f = (100 * volts - 50) * 9/5 + 32
    return (temp_degrees_f)

def dir_raw_to_degrees(dir_raw):
    degrees = dir_raw / 255 * 360
    return int(degrees)


if __name__ == "__main__":
    asyncio.run(scan(0.1))
