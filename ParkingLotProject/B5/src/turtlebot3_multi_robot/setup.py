from setuptools import setup
import os
from glob import glob

package_name = 'turtlebot3_multi_robot'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # URDF 파일 포함
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join(package_name, 'urdf', '*.urdf'))),
        # RViz 설정 파일 포함
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join(package_name, 'rviz', '*.rviz'))),
        # 런치 파일 포함
        (os.path.join('share', package_name, 'launch'), glob(os.path.join(package_name, 'launch', '*.launch.py'))),
        # World 파일 포함 (Gazebo)
        (os.path.join('share', package_name, 'worlds'), glob(os.path.join(package_name, 'worlds', '*.world'))),
        # Params 파일 포함
        (os.path.join('share', package_name, 'params'), glob(os.path.join(package_name, 'params', '*.yaml'))),
        # Models 파일 포함 (재귀적으로 모든 파일 포함)
        (os.path.join('share', package_name, 'models'), glob(os.path.join(package_name, 'models', '**', '*'), recursive=True)),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yjh',
    maintainer_email='y6hyuk@naver.com',
    description='Multi robot support TurtleBot3 in Gazebo with ROS2 Python package',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'lifting_car = turtlebot3_multi_robot.lifting_car:main',
            # 필요한 다른 노드들도 여기에 추가...
        ],
    },
)
