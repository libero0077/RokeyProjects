from setuptools import find_packages, setup

package_name = 'monitor_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
        ],
    zip_safe=True,
    maintainer='juwon',
    maintainer_email='juwon@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dual_image_publisher_node = monitor_test.dual_image_publisher:main',
            'camera_subscriber_node = monitor_test.camera_subscriber:main',
            'ui_camera_subscriber_node = monitor_test.ui_camera_subscriber:main',
            'debug_logger_node = monitor_test.debug_logger:main'
        ],
    },
)
