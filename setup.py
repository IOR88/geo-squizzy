from setuptools import setup, find_packages
import os

# TODO there is some problem with adding README.md file which have markup tokens
long_description = 'None'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
    name='geo-squizzy',
    version='0.1.dev2',
    packages=find_packages(exclude=['research*']),
    license='MIT',
    description='GeoJSON-unknown-documents-model-creation',
    long_description=long_description,
    url='https://github.com/LowerSilesians/geo-squizzy',
    author='Igor Miazek, Jakub Miazek',
    author_email='t-32@o2.pl, the@grillazz.com'
)