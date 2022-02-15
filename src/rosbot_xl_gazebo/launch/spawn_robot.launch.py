#!/usr/bin/env python3

import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution

def generate_launch_description():

  use_sim_time = LaunchConfiguration('use_sim_time', default=True)
  rosbot_xl_description = get_package_share_directory('rosbot_xl_description')
  xacro_file = os.path.join(rosbot_xl_description, 'models', 'rosbot_xl', 'rosbot_xl.urdf.xacro')


  pos_x = LaunchConfiguration('pos_x', default='0.0')
  pos_y = LaunchConfiguration('pos_y', default='0.0')
  pos_z = LaunchConfiguration('pos_z', default='0.0')

  use_sim = use_sim_time


  robot_controllers = PathJoinSubstitution(
        [
            rosbot_xl_description,
            "config",
            "controllers.yaml",
        ]
    )

    

  robot_description = {
    'robot_description' : Command([
      'xacro --verbosity 0 ', xacro_file,
      ' use_sim:=', use_sim
    ])
  }


  return LaunchDescription([

    Node(
      package='robot_state_publisher',
      executable='robot_state_publisher',
      output='screen',
      parameters=[
        {'use_sim_time': use_sim_time},
        robot_description
      ]
    ),


    Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    ),

    Node(
        package="controller_manager",
        executable="spawner",
        arguments=["velocity_controller", "--controller-manager", "/controller_manager"],
    ),

    
    Node(
      package='gazebo_ros',
      executable='spawn_entity.py',
      # output='screen',
      parameters=[{'use_sim_time': use_sim_time}],
      arguments=['-spawn_service_timeout', '600',
                 '-entity', 'rosbot_xl',
                 '-x', pos_x, '-y', pos_y, '-z', pos_z,
                 '-topic', 'robot_description']
    ),
  ])

if __name__ == '__main__':
  generate_launch_description()