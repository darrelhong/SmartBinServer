import paho.mqtt.client as mqtt
import sqlite3
import config
import os

deviceName = config.BIN_NAME

def on_client_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker to listen for nearest bin")
	else:
		print('Failed to connect, return code {:d}'.format(rc))	
		
def on_message(client, userdata, msg):
	message = msg.payload.decode()
	print("Message received: " + message)
	# parse incomming messages
	
	if (message.startswith("NEAREST_BIN_" + deviceName)):
		print("Nearest Bin received!")

		data = message.split("_")
		if (data[2] == deviceName):
			nearestBin = data[3]
			nearestBin_distance = data[4]
			c1 = conn.cursor()
			sql = 'UPDATE bin SET nearestBin = "' + nearestBin + '" , nearestBin_distance = ' + nearestBin_distance + ' WHERE bin_name = "' + deviceName + '"'

			c1.execute(sql)
			conn.commit()

try:

	#Set up DB Connection
	conn = sqlite3.connect(os.path.realpath('../instance/flaskr.sqlite'))

	#Mqtt variables
	broker = 'broker.emqx.io'
	port = 1883
	topic = "/IS4151/SmartBin/RPIBroker"
	username = 'emqx'
	password = 'public'

	#Set Connecting Client ID
	client_id_listener = f'mqtt-listener' + deviceName
	print('client_id={}'.format(client_id_listener))
	client = mqtt.Client(client_id_listener)
	client.username_pw_set(username, password)
	client.on_connect = on_client_connect
	client.connect(broker, port)
	client.subscribe(topic)
	client.on_message = on_message

	client.loop_forever()


except KeyboardInterrupt:
	print("Program terminated!")