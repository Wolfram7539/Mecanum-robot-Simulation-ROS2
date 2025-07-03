import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Define the path to the URDF file
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value=use_sim_time,
        description='Use simulation (Gazebo) clock if true'
    )
    urdf_file = os.path.join(
        get_package_share_directory('mecanum_description'),
        'urdf',
        'mecanum_robot.urdf.xacro'
    )

    sdf_file = os.path.join(
        get_package_share_directory('mecanum_description'),
        'urdf',
        'mecanum_robot.sdf'
    )

    ignition_spawn_entity = Node(
        package='ros_ign_gazebo',
        executable='create',
        output='screen',
        arguments=['-entity', 'mecanum_robot',
                   '-name', 'mecanum_robot',
                   '-file', sdf_file,
                   '-allow_renaming', 'true',
                   '-x', '0',
                   '-y', '0',
                   '-z', '0.1',
                   '-R', '0.0',
                   '-P', '0.0',
                   '-Y', '3.14'],
        )
    
    # Spawn world
    ignition_spawn_world = Node(
        package='ros_ign_gazebo',
        executable='create',
        output='screen',
        arguments=['-file', PathJoinSubstitution([
                        get_package_share_directory('mecanum_description'),
                        "worlds","warehouse", "model.sdf"]),
                   '-allow_renaming', 'false'],
        )
    # Process the URDF file with xacro
    robot_description = xacro.process_file(urdf_file).toxml()

    world_only = os.path.join(get_package_share_directory('mecanum_description'), "worlds","world_only.sdf")
    warehouse = os.path.join(get_package_share_directory('mecanum_description'), "worlds","warehouse","model.sdf")
    # Declare the robot description parameter
    robot_description_param = {'use_sim_time': use_sim_time, 'robot_description': robot_description}

    joint_state_pub = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[robot_description_param]
    )
    # Create the state publisher node
    state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description_param]
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[
                # Velocity command (ROS2 -> IGN)
                '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
                # Odometry (IGN -> ROS2)
                '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
                # TF (IGN -> ROS2)
                '/odom/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
                # Clock (IGN -> ROS2)
                '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
                # Joint states (IGN -> ROS2)
                '/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model',
                # Lidar (IGN -> ROS2)
                '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
                '/scan/points@sensor_msgs/msg/PointCloud2[ignition.msgs.PointCloudPacked',
                # IMU (IGN -> ROS2)
                '/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU',
                # Camera (IGN -> ROS2)
                '/camera/rgb/image_raw@sensor_msgs/msg/Image[ignition.msgs.Image',
                '/camera/rgb/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo',
                ],
        remappings=[
            ("/odom/tf", "tf"),
        ],
        output='screen'
    )

    map_static_tf = Node(package='tf2_ros',
                        executable='static_transform_publisher',
                        name='static_transform_publisher',
                        output='log',
                        arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'map', 'odom'])
    return LaunchDescription([
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(get_package_share_directory('ros_ign_gazebo'),
                              'launch', 'ign_gazebo.launch.py')]),
            launch_arguments={
            'ign_args': [' -r -v 3 ' + warehouse],
            'use_sim_time': use_sim_time
        }.items()),
        bridge,
        map_static_tf,
        ignition_spawn_entity,
        #ignition_spawn_world,
        declare_use_sim_time,
        state_publisher_node,
        joint_state_pub,
    ])