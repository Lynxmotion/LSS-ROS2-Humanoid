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

    return LaunchDescription([
#        SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1'),
   ])

