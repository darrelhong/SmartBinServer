import paho.mqtt.client as mqtt

name = "ALPHA"
	
def on_publisher_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker as publisher!")
	else:
		print('Failed to connect, return code {:d}'.format(rc))	

try:
	#Mqtt variables
	broker = 'broker.emqx.io'
	port = 1883
	cloudTopic = "/IS4151/SmartBin/CloudBroker"
	username = 'emqx'
	password = 'public'
	
	#Being a publisher
	client_id_publisher = f'mqtt-publisher' + name
	publisher_client = mqtt.Client(client_id_publisher)
	publisher_client.username_pw_set(username, password)
	publisher_client.on_connect = on_publisher_connect
	publisher_client.connect(broker, port)
	publisher_client.loop_start()
	
	msg = "nearest_bin_{}".format(name)
	encodedResponse = msg.encode()
	result = publisher_client.publish(cloudTopic, encodedResponse)
	status = result[0]
				
	if status == 0:
			
		print('Send {} to topic {}'.format(msg, cloudTopic))
				
	else:
			
		print('Failed to send message to topic {}'.format(cloudTopic))
	

except KeyboardInterrupt:
	print("Program terminated!")