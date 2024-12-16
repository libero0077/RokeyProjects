from setuptools import find_packages, setup

package_name = 'random_position_controller'

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
            'random_position_publisher = random_position_controller.random_position_publisher:main',
            'turtlebot_subscriber = random_position_controller.turtlebot_subscriber:main',
        ],
    },
)
