import paho.mqtt.client as paho
import random
import time
import json
import sys

# Credentials to connect to gateway MQTT broker
config= {
  "username"      : "iot_user",
  "password"      : "EcE592net!",
  "publish_topic" : "publishTemperature" ,
  "port"          : 1883
}

def on_connect(client, userdata, flags, rc):
  print("CONNECTED with code %d." % (rc))
  
def on_subscribe(client,userdata, mid, granted_qos):
  print("Subscribed: "+str(granted_qos))

def main():
  # check the correct usage of the command
  if len(sys.argv) != 2:
    print("Usage:  python sensor.py <broker IP address>")
    exit(0)

  config["broker"] = str(sys.argv[1])
  
  client = paho.Client()
  client.on_subscribe = on_subscribe
  client.on_connect = on_connect
  client.username_pw_set(config["username"],config["password"])
  client.connect(config["broker"],config["port"])

  client.loop_start()
  while True:
    temperature = random.randint(40,100)
    data = {"temperature": temperature}
    data = json.dumps(data)
    (rc, mid) = client.publish(config["publish_topic"], data)
    print("Temperature data: " + data)
    time.sleep(5)

if __name__ == '__main__':
  main()