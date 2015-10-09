from setuptools import setup, find_packages
import os
import re
import sys


if sys.version_info < (3, 1):
    raise Exception("eor-htmlgen requires Python 3.1 or higher.")

setup(name='eor-htmlgen',
    version='1.0.0',
    description='A simple HTML generator',
    long_description='',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    license='MIT',
    packages=find_packages('.', exclude=['examples*', 'test*']),
    zip_safe=True,
    install_requires=[
        'markupsafe'
    ]
)
