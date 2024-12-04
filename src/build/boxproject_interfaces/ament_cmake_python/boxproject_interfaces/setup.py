from setuptools import find_packages
from setuptools import setup

setup(
    name='boxproject_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('boxproject_interfaces', 'boxproject_interfaces.*')),
)
