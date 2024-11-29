from setuptools import find_packages, setup

package_name = 'menu_order_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/srv', ['../menu_order_interfaces/srv/MenuUpdate.srv']),  # 추가
        ('share/' + package_name + '/srv', ['../menu_order_interfaces/srv/MenuTable.srv']),  # 추가
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yjh',
    maintainer_email='y6hyuk@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'P = menu_order_project.table_order:main',
            'S = menu_order_project.kitchen_monitoring:main',
            'test_P = menu_order_project.test_order:main',
            'test_S = menu_order_project.test_sub:main',
            'test_R = menu_order_project.test_robot_controll:main',
        ],
    },
)
