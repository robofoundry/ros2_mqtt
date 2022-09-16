import os, subprocess
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess
from launch.substitutions import ThisLaunchFileDir
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')


    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('ros2_mqtt'),
        'config',
        'params.yaml'
        )

    launch_file_teleop = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [ThisLaunchFileDir(), '/teleop_twist.launch.py']
            )
        )
    relay_ros2_mqtt = Node(
        package="ros2_mqtt",
        executable="relay_ros2_mqtt",
        parameters = [config]
    )
 
    
    ld.add_action(launch_file_teleop)
    ld.add_action(relay_ros2_mqtt)


    return ld