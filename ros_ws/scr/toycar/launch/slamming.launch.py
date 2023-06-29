from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration


from launch_ros.actions import Node

import os

def generate_launch_description():

    package_name = "toycar"

    slam_dir = get_package_share_directory('slam_toolbox')
    pkg_share_dir = get_package_share_directory(package_name)

    online_async_launch = os.path.join(slam_dir,'launch','online_async_launch.py')

    param_file = os.path.join(pkg_share_dir,'config','mapper_params_online_async.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')

    localise_setting = os.path.join(pkg_share_dir,"config/veiw.rviz")

    slam = IncludeLaunchDescription(
                    PythonLaunchDescriptionSource([
                        online_async_launch]),
                        # launch_arguments={"params_file":  param_file, "use_sim_time": use_sim_time}.items()
                        launch_arguments={"slam_params_file":  param_file, 'use_sim_time': use_sim_time,}.items()
                )

    robot_spawn = IncludeLaunchDescription(
                    PythonLaunchDescriptionSource([
                        os.path.join(pkg_share_dir,"launch","robot_spawn.launch.py")]),
                        # launch_arguments={"use_sim_time": use_sim_time}.items()
                )
    rviz2 = Node(
                package="rviz2",
                executable="rviz2",
                name="rvizNode",
                output="screen",
                arguments=['-d',localise_setting]
                )
    
    return LaunchDescription([
        robot_spawn,
        slam,
        rviz2,
    ])