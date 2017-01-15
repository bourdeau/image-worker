#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='image-worker',
    version='0.0.1',
    description='Image bulk resizer using multiprocessing',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    author='Pierre-Henri Bourdeau',
    author_email='phbasic@gmail.com',
    license='MIT',
    url='https://github.com/bourdeau/image-worker',
    packages=['image-worker'],
    include_package_data=True,
    package_dir={
        '': 'src',
    },
    test_suite='tests',
    install_requires=[],
    extras_require={
        'test': (
            'coverage==3.7.1',
            'freezegun==0.3.5',
            'pylint==1.3.1',
            'pep8==1.5.7',
            'pyflakes==0.8.1',
            'coveralls==0.4.4',
        ),
    },
)
