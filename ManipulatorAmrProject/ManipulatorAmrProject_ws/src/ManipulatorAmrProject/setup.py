from setuptools import find_packages, setup

package_name = 'ManipulatorAmrProject'

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
    maintainer='juwon',
    maintainer_email='5912aa@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
       	    'webcam_node = ManipulatorAmrProject.world_camera2_node:main',
            'gui_node = ManipulatorAmrProject.ui_node:main',
            'main_node = ManipulatorAmrProject.main_node:main',
            'collect_data_node = ManipulatorAmrProject.collect_data_node:main',
            'conveyor_node = ManipulatorAmrProject.conveyor_node:main',
            'detection_grip_node = ManipulatorAmrProject.detection_grip:main',
        ],
    },
)
