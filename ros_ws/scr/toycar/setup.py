from setuptools import setup
import os
from glob import glob

package_name = 'toycar'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name , 'urdf_description/'),['urdf_description/' + 'robot.urdf.xacro']),
        (os.path.join('share', package_name , 'urdf_description/'),['urdf_description/' + 'diff_drive.xacro']),
        (os.path.join('share', package_name , 'urdf_description/'),['urdf_description/' + 'robot_core.xacro']),
        (os.path.join('share', package_name , 'urdf_description/'),['urdf_description/' + 'robot_core0.xacro']),        
        (os.path.join('share', package_name , 'urdf_description/'),['urdf_description/' + 'lidar.xacro']),
        (os.path.join('share', package_name , 'urdf_description/'),['urdf_description/' + 'inertial_macros.xacro']),
        (os.path.join('share', package_name , 'launch/'),
         glob('launch/*launch.[pxy][yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jordan',
    maintainer_email='kamurasijordanarthur@gamil.com',
    description='mobile Localisation and Obstacle Avoidence Robot',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
