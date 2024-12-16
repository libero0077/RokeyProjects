from setuptools import find_packages, setup

package_name = 'boxproject'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yjh',
    maintainer_email='y6hyuk@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'webcam_node = boxproject.web_camera_node:main',
            'gui_node = boxproject.GUI_node:main',
            'robot_status = boxproject.robot_status:main',
            'robot_arm_node = boxproject.robot_arm_node:main',
            'test_node = boxproject.debug_node:main',
            'conveyor_node = boxproject.conveyor_node:main',
        ],
    },
)
