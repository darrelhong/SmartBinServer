import paho.mqtt.client as mqtt
import time

name = "ALPHA"
	
def on_connect(client, userdata, flags, rc):
	
	if rc == 0:
	
		print("Connected to MQTT Broker!")
		
	else:
	
		print('Failed to connect, return code {:d}'.format(rc))

def run():
	try:
		#Mqtt variables
		broker = 'broker.emqx.io'
		port = 1883
		cloudTopic = "/IS4151/SmartBin/Broker"
		username = 'emqx'
		password = 'public'
		
		#Being a publisher
		client_id_publisher = 'mqtt-publisher-' + name
		client = mqtt.Client(client_id_publisher)
		print('client_id={}'.format(client_id_publisher))
		client.username_pw_set(username, password)
		client.on_connect = on_connect
		client.connect(broker, port)
		client.loop_start()
		
		"""
		msg = "{}_{}_{}_{}_{}".format(name, 0, '2021-04-16', 0, '2021-04-16')
		encodedResponse = msg.encode()
		
		#relay spill tilt
		time.sleep(1) #need this sleep if not there's no time for it to connect to the broker
		result = client.publish(cloudTopic, encodedResponse)
		status = result[0]
					
		if status == 0:
				
			print('Send {} to topic {}'.format(msg, cloudTopic))
					
		else:
				
			print('Failed to send message to topic {}'.format(cloudTopic))"""
			
			
		msg = "{}_{}_{}".format(name, 100, '2021-04-16')
		encodedResponse = msg.encode()
		
		#relay fill
		time.sleep(1) #need this sleep if not there's no time for it to connect to the broker
		result = client.publish(cloudTopic, encodedResponse)
		status = result[0]
					
		if status == 0:
				
			print('Send {} to topic {}'.format(msg, cloudTopic))
					
		else:
				
			print('Failed to send message to topic {}'.format(cloudTopic))
		

	except KeyboardInterrupt:
		print("Program terminated!")
	
if __name__ == '__main__':
	run()