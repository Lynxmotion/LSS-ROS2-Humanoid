import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node

# all hardware is on a remote Pi
print("Using bender for hardware nodes")

def generate_launch_description():
    config_dir = os.path.join(get_package_share_directory('lss_humanoid'), 'config')

    # URDF file to be loaded by Robot State Publisher
    rviz_config = os.path.join(
        get_package_share_directory('lss_humanoid'),
        'config', 'lss_humanoid.rviz'
    )

    # Robot Visualizer
    rviz_node = Node(
        name = 'rviz2',        # must match the node name in config -> YAML
        package = 'rviz2',
        executable = 'rviz2',
        output = 'screen',
        arguments = [
            '-d', rviz_config
        ]
    )

    return LaunchDescription([
        rviz_node
   ])

