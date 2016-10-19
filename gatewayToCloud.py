import paho.mqtt.client as paho
import random
import time
import json
import sys
import ibmiotf.api
import ibmiotf
import ibmiotf.device
import logging
from uuid import getnode as get_mac

# Credentials to connect to gateway MQTT broker
config= {
  "username"          : "iot_user",
  "password"          : "EcE592net!",
  "subscribe_topic"   : "publishTemperature",
  "publish_topic"     : "receivedCommand",
  "port"              : 1883
}

cloudTopic = "tempToBluemix"
previous_data = 0

def on_connect(client, userdata, flags, rc):
  print("CONNECTED with code %d." % (rc))
  client.subscribe(config["subscribe_topic"] ,1)  
  
def on_subscribe(client,userdata, mid, granted_qos):
  print("Subscribed: "+str(granted_qos))

def on_message(client, userdata, msg):
  receivedData=json.loads(msg.payload)
  if abs(receivedData["temperature"] - previous_data) > 5:
    publishData = {
      "d" : {
        "temperature" : receivedData["temperature"],
      }
    }
    cloudClient.publishEvent(cloudTopic, "json", publishData)

def myCommandCallback(cmd):
  data = json.dumps(cmd.data["status"])
  print(data)
  if int(data) == 0:
    senddata = {"ac": "off"}
  else:
    senddata = {"ac": "on"}
  senddata = json.dumps(senddata)
  (rc, mid) = client.publish(config["publish_topic"], senddata)
  print("Published a message" + senddata)

def main():
  # check the correct usage of the command
  if len(sys.argv) != 2:
    print("Usage:  python gatewayToCloud.py <broker IP address>")
    exit(0)
  
  config["broker"] = str(sys.argv[1])

  try:
    cloudOptions = {
      "org": "i5nag4",
      "type": "edison",
      "id": "myGateway",
      "auth-method": "token",
      "auth-token": "EcE592net!"
    }
    global cloudClient

    cloudClient = ibmiotf.device.Client(cloudOptions)
    cloudClient.connect()
    cloudClient.commandCallback = myCommandCallback


  except ibmiotf.ConnectionException  as e:
    print("Execption")

  global client
  client = paho.Client()
  client.on_subscribe = on_subscribe
  client.on_connect = on_connect
  client.on_message = on_message
  client.username_pw_set(config["username"],config["password"])
  client.connect(config["broker"],config["port"])

  client.loop_forever()
    
if __name__ == '__main__':
  main()