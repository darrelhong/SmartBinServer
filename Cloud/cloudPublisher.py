import paho.mqtt.client as mqtt
import time
import sqlite3
import os

name = "Cloud"
	
def on_publisher_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker as publisher!")
	else:
		print('Failed to connect, return code {:d}'.format(rc))
		
def on_client_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker to listen for RPI messages")
	else:
		print('Failed to connect, return code {:d}'.format(rc))
		

def send_message(msg):
	encodedResponse = msg.encode()
	result = publisher_client.publish(rpiTopic, encodedResponse)
	status = result[0]
				
	if status == 0:
			
		print('Send {} to topic {}'.format(msg, rpiTopic))
				
	else:
			
		print('Failed to send message to topic {}'.format(rpiTopic))

def on_message(client, userdata, msg):
	print("Received something")
	message = msg.payload.decode()
	print("Message received: " + message)
	message = message.split("_")

	#NEAREST_BIN_binName
	if (message[0] == "NEAREST"):
		print("bin {} wants to know its nearest bin".format(message[2]))
		message = "NEAREST_BIN_{}_{}_{}".format(message[2], "BRAVO", 100)
		send_message(message,)
	else:
		print("*** bin {} relaying messages up ***".format(message[0]))
		#store in db
		
		if (len(message) == 5):
			print(message)
			binName = message[0]
			is_spill = message[1]
			is_spill_updated = message[2]
			is_tilt = message[3]
			is_tilt_updated = [4]
			
			print("Storing values into TABLE bin")
			cur = conn.cursor()
			updateQuery = "UPDATE bin set is_spill = {}, is_tilt = {} WHERE bin_name = '{}'".format(is_spill, is_tilt, binName)
			cur.execute(updateQuery)
			conn.commit()
			
			
			
		elif (len(message) == 3):
			print(message)
			binName = message[0]
			fill_percent = message[1]
			time_updated = message[2]
			
			print("Storing values into TABLE fill_level")
			cur = conn.cursor()
			insertQuery = "INSERT into fill_level (fill_percent, time_updated, bin_name) VALUES ({}, {}, '{}')".format(fill_percent, time_updated, binName)
			cur.execute(insertQuery)
			conn.commit()
	
	
	#NEAREST_BIN_binName_nearestBinName_distance
	
	#relay binName_isSpill_isSpillUpdated_isTilt_isTiltUpdated;
	#relay binName_fillPercent_timeUpdated_;
		
try:
	conn = sqlite3.connect('./instance/flaskr.sqlite')
	
	#Mqtt variables
	broker = 'broker.emqx.io'
	port = 1883
	cloudTopic = "/IS4151/SmartBin/Broker"
	rpiTopic = "/IS4151/SmartBin/RPIBroker"
	username = 'emqx'
	password = 'public'
	
	
	#Being a publisher
	client_id_publisher = f'mqtt-publisher' + name
	print('client_id={}'.format(client_id_publisher))
	publisher_client = mqtt.Client(client_id_publisher)
	publisher_client.username_pw_set(username, password)
	publisher_client.on_connect = on_publisher_connect
	publisher_client.connect(broker, port)
	publisher_client.loop_start()

	#Set Connecting Client ID
	client_id_listener = f'mqtt-listener' + name
	client = mqtt.Client(client_id_listener)
	client.username_pw_set(username, password)
	client.on_connect = on_client_connect
	client.connect(broker, port)
	client.subscribe(cloudTopic)
	client.on_message = on_message

	client.loop_forever()

except KeyboardInterrupt:
	print("Program terminated!")