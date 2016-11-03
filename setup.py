#!/usr/bin/env python

from setuptools import setup


setup(
    name='qtip-cli',
    version='0.1.dev0',
    description='Platform Performance Benchmarking for OPNFV',
    author='OPNFV',
    author_email='zhang.yujunz@zte.com.cn',
    install_requires=['click'],
    packages=['cli'],
    entry_points={
        'console_scripts': ['qtip=cli.entry:cli']
    },
    license='Apache-2.0',
    keywords="performance benchmark opnfv",
    url="https://wiki.opnfv.org/display/qtip"
)
