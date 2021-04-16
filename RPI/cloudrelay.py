import time
import paho.mqtt.client as mqtt
import sqlite3
import random

name = "ALPHA"

def on_connect(client, userdata, flags, rc):
	
	if rc == 0:
	
		print("Connected to MQTT Broker!")
		
	else:
	
		print('Failed to connect, return code {:d}'.format(rc))

try :

	conn = sqlite3.connect('./instance/flaskr.sqlite')

    #Mqtt variables
	broker = 'broker.emqx.io'
	port = 1883
	cloudTopic = "/IS4151/SmartBin/CloudBroker"
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

	while True:
		time.sleep(10)

		print("Sending sensor data up to cloud now")
		c1 = conn.cursor()
		sql = "SELECT fill_percent, time_updated, bin_name, rowid FROM fill_level WHERE tocloud = 0"
		c1.execute(sql)
		results = c1.fetchall()

		c2 = conn.cursor()
		for result in results:
			fill_percent = result[0]
			time_updated = result[1]
			bin_name = result[2]
			id = result[3]
			message = bin_name + "_" +str(fill_percent) + "_" + time_updated
			message = message.encode()
			result = client.publish(cloudTopic, message)
			status = result[0]

			if status == 0 :
				print('Relayed to cloud successfully')
				print('Updating tocloud = 1 in db now')
				sql2 = "UPDATE fill_level SET tocloud = 1 WHERE rowid =?" 
				c2.execute(sql2, (str(id),))
				conn.commit()
			else:
				print('Failed to send message to topic (To cloud data) {}'.format(cloudTopic))

			
			
		conn.commit()

except KeyboardInterrupt:
	
	print('********** END')
	

finally:

	conn.close()