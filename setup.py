# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    description='CO2 Emission explorer sample app',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author='Eetu Lampsijärvi',
    url='https://github.com/Tulitomaatti/reaktor_task_a',
    download_url='https://github.com/Tulitomaatti/reaktor_task_a',
    author_email='eetu.lampsijarvi@helsinki.fi',
    version='0.1',
    install_requires=['dash', 'plotly', 'numpy', 'pandas', 'gunicorn'],
    packages=['reaktor_task_a'],
    name='reaktor_task_a',
    classifiers=[
        "Programming Language :: Python :: 2",
    ]
)
