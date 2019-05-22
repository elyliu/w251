import paho.mqtt.client as mqtt

# keeping track of the IP of the MQTT brokers
local_broker_address = "172.18.0.2"
remote_broker_address = "169.53.237.43"
topic = "test"

# subscribe to the topic on local mqtt connect
def on_connect_local(client, userdata, flags, rc):
	print("connected to local mqtt")
	client.subscribe(topic)

# just showing it connected to the cloud mqtt
def on_connect_remote(client, userdata, flags, rc):
        print("connected to remote  mqtt")

# when the local mqtt client receives new messages on the topic, publish to the cloud mqtt
def on_message(client, userdata, msg):
	remote_client.publish(topic, payload=msg.payload, qos=1, retain=False)


# setting up local mqtt client and what it should do on_connect and on_message
local_client = mqtt.Client("forwarder")
local_client.on_connect = on_connect_local
local_client.connect(local_broker_address)
local_client.on_message = on_message

# setting up connection to the mqtt on the cloud
remote_client = mqtt.Client("forwarder")  
remote_client.on_connect = on_connect_remote
remote_client.connect(remote_broker_address)

local_client.loop_forever()
