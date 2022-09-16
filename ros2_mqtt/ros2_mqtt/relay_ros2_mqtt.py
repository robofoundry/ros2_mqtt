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
        self.broker_address= self.declare_parameter("~broker_ip_address", '192.168.1.123').value
        self.MQTT_PUB_TOPIC = self.declare_parameter("~mqtt_pub_topic", 'esp32/cmd_vel').value
        self.ROS_TWIST_SUB_TOPIC = self.declare_parameter("~twist_sub_topic", '/cmd_vel').value
        self.mqttclient = mqtt.Client("ros2mqtt") 
        self.mqttclient.connect(self.broker_address) 

        self.get_logger().info('relay_ros2_mqtt:: started...')
        self.get_logger().info(f'relay_ros2_mqtt:: broker_address = {self.broker_address}')
        self.get_logger().info(f'relay_ros2_mqtt:: MQTT_PUB_TOPIC = {self.MQTT_PUB_TOPIC}')
        self.get_logger().info(f'relay_ros2_mqtt:: ROS_TWIST_SUB_TOPIC = {self.ROS_TWIST_SUB_TOPIC}')


        self.create_subscription(
            Twist,
            self.ROS_TWIST_SUB_TOPIC,
            self.publish_to_mqtt,
            qos_profile=qos_profile_system_default)


    def publish_to_mqtt(self, tmsg):
        if tmsg.linear.x != 0 or tmsg.angular.z:
            Dictionary ={'x':str(tmsg.linear.x), 'z':str(tmsg.angular.z)}
            self.get_logger().info('dict:: {0}'.format(json.dumps(Dictionary).encode()))
            
            self.mqttclient.publish(self.MQTT_PUB_TOPIC,json.dumps(Dictionary).encode(),qos=0, retain=False)

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