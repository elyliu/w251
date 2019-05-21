# cloud storage settings
credentials = {
  "apikey": "",
  "cos_hmac_keys": {
    "access_key_id": "",
    "secret_access_key": ""
  },
  "endpoints": "",
  "iam_apikey_description": "",
  "iam_apikey_name": "",
  "iam_role_crn": "",
  "iam_serviceid_crn": "",
  "resource_instance_id": ""
}
auth_endpoint = ''
service_endpoint = ''
bucket = ''

# mqtt settings
mqtt_host = ""
topic = ""

from ibm_botocore.client import Config
import ibm_boto3
import paho.mqtt.client as mqtt
import time

# on_connect we should subscribe to the topic to pull down the images
def on_connect(client, userdata, flags, rc):
    print("connected to mqtt")
    client.subscribe(topic)

# on_message save the payload to the cloud bucket
def on_message(client, userdata, msg):
    print("message received")
    png_name = "face-" + str(round(time.time()))[:-2] + ".png"
    resource.Bucket(name=bucket).put_object(Key=png_name, Body=msg.payload)
    print("wrote to bucket")

# setting up the connection to the bucket
resource = ibm_boto3.resource('s3',
                      ibm_api_key_id=credentials['apikey'],
                      ibm_service_instance_id=credentials['resource_instance_id'],
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)

# setting up mqtt connection and defining what to do on_connect and on_message
client = mqtt.Client()
client.on_connect = on_connect
client.connect(mqtt_host)
client.on_message = on_message

client.loop_forever()



