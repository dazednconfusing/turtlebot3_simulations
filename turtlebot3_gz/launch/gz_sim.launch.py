# Copyright 2022 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
import xacro

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_name = LaunchConfiguration('world_name', default='turtlebot3_world')

    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gz'), 'launch')

    static_tf = Node(package='tf2_ros',
                     executable='static_transform_publisher',
                     name='static_transform_publisher',
                     output='log',
                     arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'base_scan', [TURTLEBOT3_MODEL, '/base_footprint/hls_lfcd_lds']],
                     parameters=[{'use_sim_time': use_sim_time}])

    # Set gz-sim resource path
    gz_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH', value=[
        os.path.join(get_package_prefix('turtlebot3_description'), "share"),
        ":" +
        os.path.join(get_package_share_directory('turtlebot3_gazebo'), "models")])

    republish_cmd = Node(
        package='turtlebot3_gz',
        executable='cmd_republisher')

    gazebo_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description',
                   '-name', TURTLEBOT3_MODEL,
                   '-allow_renaming', 'true',
                   '-x', '0',
                   '-y', '0',
                    ],
        )

    return LaunchDescription([
        republish_cmd,
        static_tf,
        gz_resource_path,
        gazebo_spawn_entity,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(get_package_share_directory('ros_gz_sim'),
                              'launch', 'gz_sim.launch.py')]),
            launch_arguments=[('gz_args', [' -r -v 3 ' +
                               ' --gui-config ' +
                              os.path.join(
                                get_package_share_directory('turtlebot3_gz'),
                                "gui", "gui.config"
                              )
                             ])]),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='If true, use simulated clock'),
        DeclareLaunchArgument(
            'world_name',
            default_value=world_name,
            description='World name'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/ros_gz_bridge.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/robot_state_publisher.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/control.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/rviz.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
    ])
