from setuptools import find_packages, setup

package_name = 'my_package'

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
#    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'data_publisher = my_package.data_publisher:main',
            'data_subscriber = my_package.data_subscriber:main',
            'image_publisher = my_package.image_publisher:main',  # 추가
            'image_subscriber = my_package.image_subscriber:main',  # 추가
        ],
    },
)
