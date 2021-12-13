
import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir, LaunchConfiguration

from launch_ros.actions import Node

import xacro


def generate_launch_description():
    humanoid_pkg_dir = get_package_share_directory('lss_humanoid')
    config_dir = os.path.join(humanoid_pkg_dir, 'config')

    humanoid_config = Path(config_dir, 'humanoid.yaml')
    assert humanoid_config.is_file()

    presence_config = Path(config_dir, 'presence.yaml')
    assert presence_config.is_file()

    simulation_config = Path(config_dir, 'simulation.yaml')
    assert simulation_config.is_file()

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

    localization_node = Node(
        name='se_node',
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
        parameters=[humanoid_config, {'sim-mode': True}]
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
        arguments=['-topic', 'robot_description/gazebo',
                   '-entity', 'humanoid',
                   '-z', '0.3'],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'verbose', default_value='true',
            description='Set "true" to increase messages written to terminal.'
        ),
        DeclareLaunchArgument(
            'gui', default_value='true',
            description='Set to "false" to run headless.'
        ),
        DeclareLaunchArgument(
            'server', default_value='true',
            description='Enable if we are not debugging a plugin (where plugin is running in gzserver within gdb)'
        ),
        DeclareLaunchArgument(
            'pause', default_value='false'
        ),
        DeclareLaunchArgument(
            'world', default_value=os.path.join(humanoid_pkg_dir, 'gazebo', 'humanoid.world')
        ),
        DeclareLaunchArgument(
            'display', default_value='empty'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']
        )),

        IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(humanoid_pkg_dir, 'launch'), 
                '/rviz.launch.py']
        )),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
            [get_package_share_directory('lss_humanoid'), '/launch/', LaunchConfiguration('display'), '.launch.py']
        )),

        urdf_publisher,
        localization_node,
        spawn_entity,
        #robot_dynamics_node
    ])
