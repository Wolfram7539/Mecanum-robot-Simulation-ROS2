import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            arguments=[
                '-configuration_directory', os.path.join(get_package_share_directory('mecanum_robot_sim_launch'),'params'),
                '-configuration_basename', 'config.lua'
            ],
            parameters=[
                {'use_sim_time': False}
            ]
        ),
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[
                {'use_sim_time': False}
            ]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            parameters=[{
                # RVizの初期設定が必要なら、設定ファイルを指定することもできます
                'use_sim_time': True,
            }],
            remappings=[('/scan', '/scan'),('/imu', '/imu')]  # LIDARデータのトピック名が異なる場合にリマッピングを設定
        ),
    ])

