from setuptools import find_packages, setup

package_name = 'multi_image_package'

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
    # tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_publisher_1 = multi_image_package.image_publisher_1:main',
            'image_publisher_2 = multi_image_package.image_publisher_2:main',
            'image_subscriber = multi_image_package.image_subscriber:main',
            'image_subscriber_flask = multi_image_package.image_subscriber_flask:main',
            'amr_operating = multi_image_package.amr_operating:main',  # 추가된 노드
            'init_pose = multi_image_package.init_pose:main',  # 추가된 노드
        ],
    },
)
