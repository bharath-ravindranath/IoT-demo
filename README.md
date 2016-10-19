# IoT-demo

First setup the MQTT broker on the Gateway (Intel Edison). Then run the following codes in the order given below

# Files

logger.py  
  Runs on the gateway (Intel Edison).

  Connects to the local MQTT broker and logs all the messages received by the broker to a file

  MQTT topic    : "#"
  Logged file   : logfile

  Usage:
    python logger.py <broker IP address>

gatewayToCloud.py 
  Runs on the gateway (Intel Edison).

  Connects to both local MQTT broker and IBM Bluemix IOTF service (Bluemix MQTT Broker). Receives the data sent by the sensor. Processes the data and if appropriate sends the data to the Could

  Message format      : JSON
  Message             : {d:{temperature: <number>}}
  Bluemix MQTT topic  : "tempToBluemix"

  It also receives the commands sent by the Cloud service (NodeRED app) and sends this message to the actuator. 

  Message format    : JSON
  Message           : {d:{"status": 0/1}}      <0/1 indicates to switch on/off AC>
  Local MQTT message: {"ac": "on/off"}
  Local MQTT topic  : "receivedCommand"

  Usage:
    python gatewayToCloud.py <broker IP address>

sensor.py
  Runs on the sensor.
  
  Connects the local MQTT broker running on the Intel Edison gateway. Sends a random number between 40 and 100 every 5 seconds in the JSON format - {"temperature": <number>}

  Message format: JSON
  Message       : integer between 40 and 100
  Time Interval : 5 sec
  MQTT topic    : "publishTemperature"

  Usage:
    python sensor.py <broker IP address>

actuator.py  
  Runs on the actuator.

  Connects to local MQTT broker. Turns on/off the AC according to the command received from the gateway.

  Received message    : {"ac": "on/off"}
  MQTT broker topic   : "receivedCommand"

  Usage:
    python actuator.py <broker IP address>
