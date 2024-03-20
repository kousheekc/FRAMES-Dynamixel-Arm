from launch import LaunchDescription
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ld = LaunchDescription()

    urdf_dir = FindPackageShare('frames_description')
    urdf_path = PathJoinSubstitution([urdf_dir, 'urdf', 'frames.urdf'])
    bringup_dir = FindPackageShare('frames_bringup')
    rviz_config_path = PathJoinSubstitution([bringup_dir, 'config', 'urdf.rviz'])

    robot_description_content = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    ld.add_action(DeclareLaunchArgument(
        name='gui', 
        default_value='false', 
        choices=['true', 'false'], 
        description='Flag to enable joint_state_publisher_gui'
        ))

    ld.add_action(Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description_content,
        }]))

    ld.add_action(Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    ))

    ld.add_action(Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
    ))
    return ld