from setuptools import find_packages
from setuptools import setup

setup(
    name='menu_order_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('menu_order_interfaces', 'menu_order_interfaces.*')),
)
