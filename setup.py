## -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='planogram',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Emily Ahlquist',
    author_email='lunarosemanor@gmail.com',
    url='https://github.com/LunaRoseManor/planogram',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
