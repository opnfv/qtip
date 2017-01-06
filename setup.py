#!/usr/bin/env python

from setuptools import setup

requirements = open('requirements.txt')

setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
    install_requires = requirements.read().splitlines(),
)
