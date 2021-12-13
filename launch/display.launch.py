#!/usr/bin/python3

import os
import sys
from pathlib import Path
import launch

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node, LifecycleNode
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir, LaunchConfiguration


def generate_launch_description():

    # Launch Description
    ld = launch.LaunchDescription()

    # Set LOG format
    os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time}: [{name}] [{severity}]\t{message}'

    config_dir = os.path.join(get_package_share_directory('lss_humanoid'), 'config')

     # URDF file to be loaded by Robot State Publisher
    humanoid_urdf = os.path.join(
        get_package_share_directory('lss_humanoid'),
            'urdf', 'lss_humanoid.urdf'
    )

    humanoid_config = Path(config_dir, 'humanoid.yaml')
    assert humanoid_config.is_file()

    presence_config = Path(config_dir, 'presence.yaml')
    assert presence_config.is_file()

    # dummy laser to set the world transform
    #map_node = Node(
    #    node_name = 'lss_dummy_map_server',        # must match the node name in config -> YAML
    #    package = 'lss_joint_publisher',
    #    node_executable = 'lss_dummy_map_server',
    #    output = 'screen'
    #)

    urdf_publisher = Node(
        package='resource_publisher',
        executable='resource_publisher',
        output='screen',
        arguments=[
            '-package', 'lss_humanoid',
            '-xacro', 'urdf/lss_humanoid.xacro.urdf',
            '-topic', 'robot_description',
            '-targets', '*,gazebo']
    )

    # Robot State Publisher
    # URDF publishing is now provided by resource_publisher and TF is provided by robot_dynamics
    #rsp_node = Node(
    #    node_name = 'humanoid_state_publisher',        # must match the node name in config -> YAML
    #    package = 'robot_state_publisher',
    #    node_executable = 'robot_state_publisher',
    #    output = 'screen',
    #    arguments = [humanoid_urdf]
    #)

    localization = Node(
        name='localization',
        package='robot_localization',
        executable='se_node',
        output='screen',
        parameters=[presence_config],
        remappings=[
            ('odometry/filtered', 'odom')
        ]
    )

    robot_dynamics_node = Node(
        name="robot_dynamics",
        package='humanoid_dynamic_model',
        executable='robot_dynamics',
        output='screen',
        parameters=[humanoid_config, {'sim-mode': False}]
    )

    #laser_node =  Node(package='dummy_sensors', node_executable='dummy_laser', output='screen')

    # see this file for one way to start ros2 controllers
    # https://github.com/ros-planning/moveit2/blob/main/moveit_ros/moveit_servo/launch/servo_cpp_interface_demo.launch.py


    ld.add_action( launch.actions.DeclareLaunchArgument('hardware', default_value='hardware') )
    ld.add_action( launch.actions.DeclareLaunchArgument('display', default_value='empty') )
    ld.add_action( IncludeLaunchDescription(PythonLaunchDescriptionSource([ThisLaunchFileDir(),'/',LaunchConfiguration('hardware'), '.launch.py'])) )
    ld.add_action( IncludeLaunchDescription(PythonLaunchDescriptionSource([ThisLaunchFileDir(),'/',LaunchConfiguration('display'), '.launch.py'])) )
    #ld.add_action( map_node )
    ld.add_action( urdf_publisher )
    #ld.add_action( rsp_node )
    #ld.add_action( localization )
    #ld.add_action( robot_dynamics_node )
    #ld.add_action( laser_node )

    return ld



