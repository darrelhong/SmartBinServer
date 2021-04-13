import serial
import time
import sqlite3
import socket
import _thread as thread
import paho.mqtt.client as mqtt
import random
import _thread as thread
import os

from datetime import datetime

from gpiozero import MCP3008
from gpiozero import PWMLED

# Import local config
import config

deviceName = config.BIN_NAME

# periodically call central to request for info.

def sendCommand(command):
		
	command = command + '\n'
	ser.write(str.encode(command))


def waitResponse():
	
	response = ser.readline()
	response = response.decode('utf-8').strip()
	
	return response

def on_connect(client, userdata, flags, rc):
	
	if rc == 0:
	
		print("Connected to MQTT Broker!")
		
	else:
	
		print('Failed to connect, return code {:d}'.format(rc))

def saveToDB2():
    #place holder
    print("Placeholder for db data.")

def saveToDB():
    c = conn.cursor()
    for sensorValue in listSensorValues:
        deviceName = sensorValue.split("_")[0]
        temp = sensorValue.split("_")[1]
        light = sensorValue.split("_")[2]

        if (float(temp) >=40 and float(light) >= 80):
            hasFire =  "1"
        else:
            hasFire = "0"
            #jst for debug
            #sendFireAlert(deviceName)

        print("Saving -> " + deviceName + ": " + temp + " , " + light)
        sql = "INSERT INTO hub_sensor (devicename, temp, light, hasFire, timestamp) VALUES('" + deviceName + "', " + temp + " ," + light +" ," + hasFire + ", datetime('now', 'localtime'))"
        c.execute(sql)
    conn.commit()

def takePicture():
    # threaded message
    # take camera and return a value
    # return a success or fail reply.
    print("Camera module called.")
    time.sleep(13)
    #return true
    sendCommand("cmd:" + deviceName + "_BDOOR_1")
    print("sending return msg from thread")
try:

    host = socket.gethostname()
    port = 9999

    #s = socket.socket()
    #s.connect((host, port))

    #message = "INIT_RPI_SENSOR"

    #RPI.. either ACM0 or ACM01
    print("Listening on /dev/ttyACM2... Press CTRL+C to exit")	
    ser = serial.Serial(port='/dev/ttyACM2', baudrate=115200, timeout=1)
    print("Device Name: " + deviceName)
    
    #Win10
    #print("Listening on COM7.. Press CTRL + C to exit program")
    #ser = serial.Serial(port='COM7', baudrate=115200, timeout=1)

    conn = sqlite3.connect(os.path.realpath('../instance/flaskr.sqlite'))

	# Handshaking
    sendCommand('handshake')
	
    strMicrobitDevices = ''
	
    while strMicrobitDevices == None or len(strMicrobitDevices) <= 0:
		
        strMicrobitDevices = waitResponse()
        time.sleep(0.1)
	
    testTemp = strMicrobitDevices
    strMicrobitDevices = strMicrobitDevices.split('=')
    
    print(testTemp)
    if len(strMicrobitDevices[1]) > 0:

        listMicrobitDevices = strMicrobitDevices[1].split(',')
		
        if len(listMicrobitDevices) > 0:
				
            for mb in listMicrobitDevices:
			
                print('Connected to micro:bit device: {} ...'.format(mb))
			
            while True:
				
                commandToTx = "SENSOR_" + deviceName
                sendCommand('cmd:' + commandToTx)
                print('Finished sending command [cmd:' + commandToTx + '] to all micro:bit devices...')
                
                if commandToTx.startswith('SENSOR_'):
                
                    strSensorValues = ''
                    
                    while strSensorValues == None or len(strSensorValues) <= 0:
                        
                        incomingData = waitResponse()
                        print("****"+ incomingData)
                        if (incomingData.startswith(deviceName + "_TDOOR")):
                            #Start new thread.
                            print("test")
                            thread.start_new_thread(takePicture, ())

                        else :     
                            strSensorValues = incomingData
                        
                        time.sleep(0.1)
                    
                    listSensorValues = strSensorValues.split(',')
        
                    print("Before going to db2.. " + str(listSensorValues))
                    #saveToDB()
                    saveToDB2()
                time.sleep(0.1)
	
except KeyboardInterrupt:

    if ser.is_open:
        ser.close()
    	
    print("Program terminated!")