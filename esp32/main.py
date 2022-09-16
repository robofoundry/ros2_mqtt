# main.py

### --- same as before ---
from umqtt.simple import MQTTClient
from machine import Pin
import json
import sys
import machine
from time import sleep
led = machine.Pin(2, machine.Pin.OUT)
msg = ""
# mqtt client setup
CLIENT_NAME = 'esp32'
BROKER_ADDR = 'IP_ADDR_OF_MQTT_BROKER'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()

TWIST_TOPIC = b'esp32/cmd_vel'
val = True
def handle_twist_msg(topic, msg):
    global val
    led.value(int(val))
    print(msg.decode())
    twist = json.loads(msg.decode()) 
    print('x={0} z={1}'.format(twist['x'], twist['z']))
    val = not val
    
# mqtt subscription
mqttc.set_callback(handle_twist_msg)
mqttc.subscribe(TWIST_TOPIC)

while True:
    mqttc.check_msg()
    sleep(0.1)
