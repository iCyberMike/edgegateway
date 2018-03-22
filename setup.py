#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

#from distutils.core import setup
from setuptools import setup, find_packages

package_name = 'edgegateway'
filename = package_name + '.py'


def get_version():
    import ast

    with open(filename) as input_file:
        for line in input_file:
            if line.startswith('_version'):
                return ast.parse(line).body[0].value.s

def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''


setup(
    name='edgegateway',
    version=get_version(),
    description='Edge Gateway GPIO and MQTT message processing',
    long_description=get_long_description(),
    author='mtelep',
    author_email='mtelep33@gmail.com',
    url='https://www.avantia-inc.com/',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=['paho-mqtt>=1.3'],
    python_requires='>=3',
     
#    py_modules=[package_name],
#     packages=['funniest'],
#      install_requires=[
#          'markdown',
#      ],
    entry_points={
        'console_scripts': [
            'edgegateway = edgegateway.edgegateway:main',
            'edgerun = edgegateway.edgegateway:run'
        ]
    },
    license='License ::  MIT License',
)