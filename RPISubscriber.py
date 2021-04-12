import paho.mqtt.client as mqtt

name = "ALPHA"
	
def on_publisher_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker as publisher!")
	else:
		print('Failed to connect, return code {:d}'.format(rc))	
		
def on_client_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker to listen for nearest bin")
	else:
		print('Failed to connect, return code {:d}'.format(rc))	
		
def on_message(client, userdata, msg):
	message = msg.payload.decode()
	print("Message received: " + message)
	print("Close client connection")
	client.disconnect()


try:
	#Mqtt variables
	broker = 'broker.emqx.io'
	port = 1883
	topic = "/IS4151/SmartBin/Broker"
	username = 'emqx'
	password = 'public'
	
	#Being a publisher
	client_id_publisher = f'mqtt-publisher' + name
	publisher_client = mqtt.Client(client_id_publisher)
	publisher_client.username_pw_set(username, password)
	publisher_client.on__connect = on_publisher_connect
	publisher_client.connect(broker, port)
	publisher_client.loop_start()
	
	msg = "nearest_bin_{}".format(name)
	msg = msg.encode()
	result = publisher_client.publish(topic, msg)
	status = result[0]
			
	if status == 0:
			
		print('Send {} to topic {}'.format(msg, topic))
				
	else:
			
		print('Failed to send message to topic {}'.format(topic))
	
	
	

	#Set Connecting Client ID
	client_id_listener = f'mqtt-listener' + name
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