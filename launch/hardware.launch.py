import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node

import xacro


def generate_launch_description():
    config_dir = os.path.join(get_package_share_directory('lss_humanoid'), 'config')

    hardware_config = Path(config_dir, 'hardware.yaml')
    assert hardware_config.is_file()

    #humanoid_urdf = os.path.join(
    #    get_package_share_directory('lss_humanoid'),
    #        'urdf', 'lss_humanoid.urdf'
    #)
    # Get URDF via xacro
    robot_description_path = os.path.join(
        get_package_share_directory('lss_humanoid'),
        'urdf',
        'lss_humanoid.xacro.urdf')
    robot_description_config = xacro.process_file(robot_description_path)
    robot_description = {'robot_description': robot_description_config.toxml()}

    return LaunchDescription([
#        SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1'),
        # Joint State Publisher
        #Node(
        #    node_name = 'lss_joint_controller',
        #    package = 'lss_joint_publisher',
        #    node_executable = 'lss_joint_controller',
        #    output = 'screen',
        #    parameters=[hardware_config]
        #),

        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[robot_description, hardware_config],
            output={
                'stdout': 'screen',
                'stderr': 'screen',
            },
        ),

        # IMU
        Node(
            name="imu",
            package='bno055_driver',
            executable='bno055_driver',
            output='screen',
            parameters=[hardware_config]
        )
    ])

