from setuptools import find_packages, setup

package_name = 'turtlebot3_python_nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/srv', ['../turtlebot3_interfaces/srv/ExitRequest.srv']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rokey',
    maintainer_email='libero0077@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'gui_minimap = turtlebot3_python_nodes.gui_minimap:main',
            'central_control_node = turtlebot3_python_nodes.central_control_node:main',
            'kiosk_gui = turtlebot3_python_nodes.kiosk_gui:main',
        ],
    },
)
