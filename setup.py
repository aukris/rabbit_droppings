#!/usr/bin/env python

from setuptools import setup

NAME = "rabbit_utils"
VERSION = "0.1.0"
SCRIPTS = [
    'bin/rabbit_droppings',
]

setup(
    author='aukris',
    author_email='abhijith@tapchief.com',
    description='Backup/Restore/Remove Job from RabbitMQ queues',
    install_requires=[
        # Pika does not use semantic versioning.  Breaking changes may
        # be introduced with a bump in patch level, which is why we
        # ask for an exact patch level.
        "pika==0.9.14",
    ],
    keywords = "rabbit rabbitmq backup restore remove job",
    name=NAME,
    packages=['rabbit_droppings'],
    scripts=SCRIPTS,
    test_suite="tests",
    url="https://github.com/aukris/rabbit_droppings",
    version=VERSION,
)
