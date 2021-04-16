import serial
import time
import sqlite3
import socket
import _thread as thread
import paho.mqtt.client as mqtt
import random
import _thread as thread
import os
from waste_classifier.waste_classifier import WasteClassifier

from datetime import datetime

from gpiozero import MCP3008
from gpiozero import PWMLED

# Import local config
import config

deviceName = config.BIN_NAME
cameraOn = False
ULTRASONIC_FRONT_EMPTY = 39
ULTRASONIC_FRONT_FULL = 21

ULTRASONIC_BACK_EMPTY = 25
ULTRASONIC_BACK_FULL = 15

FILL_TRESHOLD = (ULTRASONIC_FRONT_EMPTY - ULTRASONIC_FRONT_FULL) + (ULTRASONIC_BACK_EMPTY - ULTRASONIC_BACK_FULL)
# periodically call central to request for info.

def sendCommand(command):
		
	command = command + '\n'
	ser.write(str.encode(command))


def waitResponse():
	
	response = ser.readline()
	response = response.decode('utf-8').strip()
	
	return response

def on_publisher_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker as publisher!")
	else:
		print('Failed to connect, return code {:d}'.format(rc))	

def checkNearestBin():
    
	broker = 'broker.emqx.io'
	port = 1883
	topic = "/IS4151/SmartBin/CloudBroker"
	username = 'emqx'
	password = 'public'
	
	#Being a publisher
	client_id_publisher = f'mqtt-publisher' + deviceName
	publisher_client = mqtt.Client(client_id_publisher)
	publisher_client.username_pw_set(username, password)
	publisher_client.on__connect = on_publisher_connect
	publisher_client.connect(broker, port)
	publisher_client.loop_start()
	
	msg = "nearest_bin_{}".format(deviceName)
	msg = msg.encode()
	result = publisher_client.publish(topic, msg)
	status = result[0]
			
	if status == 0:
			
		print('Send {} to topic {}'.format(msg, topic))
				
	else:
			
		print('Failed to send message to topic {}'.format(topic))
		
def saveToDB2():
    #place holder
    #print("Placeholder for db data.")
    c = conn.cursor()
    for sensorValue in listSensorValues:
        data = sensorValue.split("_")
        incomingDeviceName = data[0]
        if (incomingDeviceName == deviceName):
            sensorName = data[1]
            if (sensorName == "FILL"):
                # fill level has level data[2] and data[3]
                fillFront = int(data[2])
                fillBack = int(data[3])
                
                percentage = round(((((ULTRASONIC_FRONT_EMPTY - fillFront) + (ULTRASONIC_BACK_EMPTY - fillBack))/FILL_TRESHOLD) * 100),2)
                sql = "INSERT INTO fill_level(fill_percent, bin_name) VALUES(" + str(percentage) + ",'ALPHA');"
                #print("fill.")

                if ( percentage > 70 ) :
                    checkNearestBin()
                
                
            elif (sensorName == "TILT"):
                #print("tilted")
                hasTilt = data[2]
                sql = "UPDATE bin SET is_tilt = " + hasTilt + " WHERE bin_name = 'ALPHA'"
                #print(sql)
                
            elif (sensorName == "WATER"):
                #print("water")
                hasSpill = data[2]
                sql = "UPDATE bin SET is_spill = " + hasSpill + " WHERE bin_name = 'ALPHA'"
                #print(sql)
            
            c.execute(sql)
            conn.commit()
            
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
    global cameraOn
    if (cameraOn == False):
        cameraOn = True
        time.sleep(5)
        print("****  ITEM DETECTED... CAMERA MODULE CALLED ****.")
        wc = WasteClassifier("waste_classifier/model")
        result = wc.classify()
    
        print("**** WASTE CLASSIFIER RESULT: " + result + " ****")
    
    #time.sleep(13)
    #return true
        sendCommand("cmd:" + deviceName + "_BDOOR_1")
        cameraOn = False
    else :
        print("Camera is ongoing please wait...")

try:

    host = socket.gethostname()
    port = 9999

    #s = socket.socket()
    #s.connect((host, port))

    #message = "INIT_RPI_SENSOR"

    #RPI.. either ACM0 or ACM01
    print("Listening on /dev/ttyACM1... Press CTRL+C to exit")	
    ser = serial.Serial(port='/dev/ttyACM1', baudrate=115200, timeout=1)
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
                        #print("****"+ incomingData)
                        if (incomingData.startswith(deviceName + "_TDOOR")):
                            #Start new thread.
                            thread.start_new_thread(takePicture, ())

                        else :     
                            strSensorValues = incomingData
                        
                        time.sleep(0.1)
                    
                    listSensorValues = strSensorValues.split(',')
        
                    #print("Before going to db2.. " + str(listSensorValues))
                    #saveToDB()
                    saveToDB2()
                time.sleep(0.1)
	
except KeyboardInterrupt:

    if ser.is_open:
        ser.close()
    	
    print("Program terminated!")