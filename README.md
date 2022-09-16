### ros2_mqtt
### A ros2 node that listens to teleop_twist message and publishes to mqtt topic

### on computer

### update configurations in following places
1. in ros2_mqtt/config/param.yaml file - replace 192.168.1.123 with ip address of where you are running mqtt broker [your computer]
2. in esp32/boot.py - update SSID and PWD for your wifi
3. in esp32/main.py - replace IP_ADDR_OF_MQTT_BROKER with your mqtt broker ip address [same as ####1]

### build the project from root folder of workspace
colcon build

### launch the ros2mqtt node along with teleop twist nodes
ros2 launch ros2_mqtt ros2_mqtt.launch.py

### show twist messages
ros2 topic echo /cmd_vel

### show mqtt messages
mosquitto_sub -v -t 'esp32/cmd_vel'

### restart mqtt broker
sudo systemctl stop snap.mosquitto.mosquitto.service
sudo systemctl start snap.mosquitto.mosquitto.service


### on ESP32

### install Thonny and set interpreter to esp32
### connect esp32 via usb to your computer
### install esptool and flash micropython on esp32

### upload boot.py and main.py files on esp32 and connect with esp32 again

### you should be able to send twist messages using joystick and should be able to confirm
### those messages are being published to mqtt topic by subscribing to mqtt topic
### and looking at the console log on Thonny where esp32 will log same messages