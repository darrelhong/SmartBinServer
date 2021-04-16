import paho.mqtt.client as mqtt

name = "ALPHA"

def on_client_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker to listen for nearest bin")
	else:
		print('Failed to connect, return code {:d}'.format(rc))	

def on_message(client, userdata, msg):
	message = msg.payload.decode()
	print("Message received: " + message)

try:
	#Mqtt variables
	broker = 'broker.emqx.io'
	port = 1883
	rpiTopic = "/IS4151/SmartBin/RPIBroker"
	username = 'emqx'
	password = 'public'
	
	#Set Connecting Client ID
	client_id_listener = f'mqtt-listener' + name
	print('client_id={}'.format(client_id_listener))
	client = mqtt.Client(client_id_listener)
	client.username_pw_set(username, password)
	client.on_connect = on_client_connect
	client.connect(broker, port)
	client.subscribe(rpiTopic)
	client.on_message = on_message

	client.loop_forever()
	

except KeyboardInterrupt:
	print("Program terminated!")