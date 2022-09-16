#!/usr/bin/env python3

import rclpy
from rclpy.time import Time

from time import sleep
import sys
import threading
import numpy as np
import os
import paho.mqtt.client as mqtt
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from rclpy.qos import qos_profile_services_default

from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Twist
#from geometry_msgs.msg import Point, Pose, Quaternion, Vector3
from std_msgs.msg import Int32, Float32

import json

class RelayRos2Mqtt(Node):
    def __init__(self):
        super().__init__('relay_ros2_mqtt')
        
        self.sleep_rate = 0.025
        self.rate = 10
        self.r = self.create_rate(self.rate)
        broker_address="192.168.1.145" 
        self.mqttclient = mqtt.Client("ros2mqtt") #create new instance
        self.mqttclient.connect(broker_address) #connect to broker

        self.get_logger().info('relay_ros2_mqtt:: started...')


        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.publish_to_mqtt,
            qos_profile=qos_profile_system_default)


        # self._lock = threading.Lock()
        # self.thread = threading.Thread(target=self.calibrate_manual)
        # self.thread.start()

    def publish_to_mqtt(self, tmsg):
        if tmsg.linear.x != 0 or tmsg.angular.z:
            TEST_TOPIC = 'esp32/cmd_vel'
            Dictionary ={'x':str(tmsg.linear.x), 'z':str(tmsg.angular.z)}
            #json_str = ('{"x":"{0}", "z":"{1}"}'.format(str(tmsg.linear.x), str(tmsg.angular.z)))
            self.get_logger().info('dict:: {0}'.format(json.dumps(Dictionary).encode()))
            
            self.mqttclient.publish(TEST_TOPIC,json.dumps(Dictionary).encode(),qos=0, retain=False)#publish

def main(args=None):
    

    rclpy.init(args=args)
    try:
        relay_ros2_mqtt = RelayRos2Mqtt()
        rclpy.spin(relay_ros2_mqtt)
    except rclpy.exceptions.ROSInterruptException:
        pass

    relay_ros2_mqtt.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()