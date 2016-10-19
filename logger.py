import paho.mqtt.client as paho
import random
import time
import json

# Credentials to connect to gateway MQTT broker
config= {
  "username"          : "iot_user",
  "password"          : "EcE592net!",
  "subscribe_topic"   : "#",
  "port"              : 1883
}

def on_connect(client, userdata, flags, rc):
  print("CONNECTED with code %d." % (rc))
  client.subscribe(config["subscribe_topic"] ,1)
  
def on_subscribe(client,userdata, mid, granted_qos):
  print("Subscribed: "+str(granted_qos))

def on_message(client, userdata, msg):
  with open('logfile','a+') as file:
    file.write("Topic: " + msg.topic +"  Data: "+ str(msg.payload)+"\n")

def main():
  # check the correct usage of the command
  if len(sys.argv) != 2:
    print("Usage:  python logger.py <broker IP address>")
    exit(0)
  
  config["broker"] = str(sys.argv[1])
  client = paho.Client()
  client.on_subscribe = on_subscribe
  client.on_connect = on_connect
  client.on_message = on_message
  client.username_pw_set(config["username"],config["password"])
  client.connect(config["broker"],config["port"])

  client.loop_forever()
    
if __name__ == '__main__':
  main()