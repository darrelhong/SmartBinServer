import paho.mqtt.client as mqtt
import time

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
		

def send_message(msg, client):
	encodedResponse = msg.encode()
	result = client.publish(rpiTopic, encodedResponse)
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
		print("bin {} wants to know its nearest bin".format(message[1]))
	else:
		print("Relay messages up")
	
	
	
	
	#NEAREST_BIN_binName_nearestBinName_distance
	response = "nearest_bin_ALPHA_BRAVO_100_20"
	
	
	#relay binName_isSpill_isSpillUpdated_isTilte_isTileUpdated;
	#relay binName_fillPercent_timeUpdated_;
	
	#do some processing
	msg = ""
	
	send_message(msg, rpiTopic)
		
			



try:
	
	#Mqtt variables
	broker = 'broker.emqx.io'
	port = 1883
	cloudTopic = "/IS4151/SmartBin/CloudBroker"
	rpiTopic = "/IS4151/SmartBin/RPIBroker"
	username = 'emqx'
	password = 'public'
	
	"""
	#Being a publisher
	client_id_publisher = f'mqtt-publisher' + name
	print('client_id={}'.format(client_id_publisher))
	publisher_client = mqtt.Client(client_id_publisher)
	publisher_client.username_pw_set(username, password)
	publisher_client.on_connect = on_publisher_connect
	publisher_client.connect(broker, port)
	publisher_client.loop_start()"""

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