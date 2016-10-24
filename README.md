# IoT-demo

## Introduction

First setup the MQTT broker on the Gateway (Intel Edison). Then run the following codes in the order given below

## MQTT Broker Setup

### Installing Mosquitto MQTT Broker on Intel Edison

Mosquitto is an Open Source MQTT server/broker. It accepts data from a publisher and distributes it to all subscribers. 

Note: There are issues with mosquitto 1.4 installation on Intel Edison. So we will be using the older version 1.3

Use the following commands to install prerequisites 
```
sudo apt-get update
sudo apt-get install build-essential libwrap0-dev libssl-dev libc-ares-dev uuid-dev xsltproc
```

Download the Mosquitto MQTT server using:
```
wget http://mosquitto.org/files/source/mosquitto-1.3.5.tar.gz
```
Or
```
wget http://mosquitto.org/files/source/mosquitto-1.4.9.tar.gz
```
Unzip:
```
tar xvzf mosquitto-1.3.5.tar.gz
```
Install using the following commands
```
cd mosquitto-1.3.5

sudo su

Install the mosquitto package
make WITH_SRV=no
make install
```

Copy mosquitto files to /usr/bin to access this using PATH variable. (Alternate is to add the current directory to PATH variable)
```
cp client/mosquitto_sub /usr/bin
cp client/mosquitto_pub /usr/bin
cp lib/libmosquitto.so.1 /usr/lib
cp src/mosquitto /usr/bin
```

Create the mosquitto_usr user (The default user used by the mosquitto broker. So you can add that. Or you can use any user and specify that in the configuration file given below):
```
useradd mosquitto_usr
```

We create password for a user (test_user) (This is the username and password used for the mqtt connection (authentication for mqtt). This is not the user on the local machine)
```
mosquitto_passwd -c /etc/mosquitto/pwfile test_user
```

Create a directory for database files of mqtt broker
```
mkdir /var/lib/mosquitto
chown mosquitto_usr:mosquitto_usr /var/lib/mosquitto -R
```

Create a configuration file to configure broker
```
cat <<EOF > /etc/mosquitto/mosquitto.conf
listener 1883 <your IP>
persistence true
persistence_location /var/lib/mosquitto/
persistence_file mosquitto.db
user mosquitto_usr
log_dest syslog
log_dest stdout
log_dest topic
log_type error
log_type warning
log_type notice
log_type information
connection_messages true
log_timestamp true
allow_anonymous false
password_file /etc/mosquitto/pwfile
EOF
```

Load the new configuration using
```
/sbin/ldconfig
```

Run the Mosquitto broker:
```
mosquitto -c /etc/mosquitto/mosquitto.conf
```

### Test the broker

Use the test scripts provided by mosquitto to test the broker.

On a separate ssh terminal run the subscriber script using:
```
mosquitto_sub -h <broker_IP> -p 1883 -v -t ‘newtopic/#’ -u test_user -P <your password>
```

Open another ssh terminal window and publish a message to the same topic:
```
mosquitto_pub -h <broker_IP> -p 1883 -t ‘newtopic/1’ -m “This is a test message” -u test_user -P <your_passwd>
```

On the terminal running subscriber you should see the message “This is a test message”. 

At this point we have tested that the broker is installed correctly and can receive message from a publisher and send messages to subscribers.

Now we will move on the publishing and subscribing using a Python code.
Use ‘pip install paho-mqtt’ on the edison board to install the necessary python libraries (paho.mqtt)

## Files

* logger.py  

  Runs on the gateway (Intel Edison).

  Connects to the local MQTT broker and logs all the messages received by the broker to a file
  ```
  MQTT topic    : "#"
  Logged file   : logfile
  ```

  
  Usage:
  ```
  python logger.py <broker IP address>
  ```

* gatewayToCloud.py 

  Runs on the gateway (Intel Edison).

  Connects to both local MQTT broker and IBM Bluemix IOTF service (Bluemix MQTT Broker). Receives the data sent by the sensor. Processes the data and if appropriate sends the data to the Could

  ```
  Message format      : JSON
  Message             : {d:{temperature: <number>}}
  Bluemix MQTT topic  : "tempToBluemix"
  ```

  It also receives the commands sent by the Cloud service (NodeRED app) and sends this message to the actuator. 
  ```
  Message format    : JSON
  Message           : {d:{"status": "Temperature safe turn OFF AC"/"Temperature criticle turn ON AC"}}     
  Local MQTT message: "0"/"1"     // Sending to actuator
  Local MQTT topic  : "receivedCommand"
  ```
  Usage:
  ```
  python gatewayToCloud.py <broker IP address>
  ```

* sensor.py

  Runs on the sensor.
  
  Connects the local MQTT broker running on the Intel Edison gateway. Sends a random number between 40 and 100 every 5 seconds in the JSON format - {"temperature" : \<number\> }
  ```
  Message format: JSON
  Message       : integer between 40 and 100
  Time Interval : 5 sec
  MQTT topic    : "publishTemperature"
  ```

  Usage:
  ```
  python sensor.py <broker IP address>
  ```

* actuator.py  

  Runs on the actuator.

  Connects to local MQTT broker. Turns on/off the AC according to the command received from the gateway.
  ```
  Received message    : "0"/"1"
  MQTT broker topic   : "receivedCommand"
  ```
  Usage:
  ```
  python actuator.py <broker IP address>
  ```
