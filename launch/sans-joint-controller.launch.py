#!/usr/bin/python3

import os
import sys
from pathlib import Path
import launch

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node, LifecycleNode
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir


def generate_launch_description():

    # Launch Description
    ld = launch.LaunchDescription()

    # Set LOG format
    os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time}: [{name}] [{severity}]\t{message}'

    config_dir = os.path.join(get_package_share_directory('lss_humanoid'), 'config')

     # ZED-M URDF file to be loaded by Robot State Publisher
    humanoid_urdf = os.path.join(
        get_package_share_directory('lss_humanoid'),
            'urdf', 'lss_humanoid.urdf'
    )
    #assert humanoid_urdf.is_file()

    rviz_config = Path(config_dir, 'lss_humanoid.rviz').resolve()
    assert rviz_config.is_file()

    joints_config = os.path.join(config_dir, 'joints.yaml')
    #assert joints_config.is_file()

    presence_config = Path(config_dir, 'presence.yaml')
    assert presence_config.is_file()

    # dummy laser to set the world transform
    laser_node = Node(
        node_name = 'lss_dummy_laser',        # must match the node name in config -> YAML
        package = 'lss_joint_publisher',
        node_executable = 'lss_dummy_laser',
        output = 'screen'
    )

    # dummy laser to set the world transform
    map_node = Node(
        node_name = 'lss_dummy_map_server',        # must match the node name in config -> YAML
        package = 'lss_joint_publisher',
        node_executable = 'lss_dummy_map_server',
        output = 'screen'
    )

    # Robot State Publisher
    rsp_node = Node(
        node_name = 'humanoid_state_publisher',        # must match the node name in config -> YAML
        package = 'robot_state_publisher',
        node_executable = 'robot_state_publisher',
        output = 'screen',
        arguments = [humanoid_urdf]
    )

    # Robot Visualizer
    rviz_node = Node(
        node_name = 'rviz2',        # must match the node name in config -> YAML
        package = 'rviz2',
        node_executable = 'rviz2',
        output = 'screen',
        arguments = [
             '--display-config', str(rviz_config)
        ]
    )

    ld.add_action( map_node )
    ld.add_action( rsp_node )
    ld.add_action( laser_node )
    ld.add_action( rviz_node )

    return ld



