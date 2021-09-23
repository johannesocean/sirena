# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).
"""
Created on 2021-02-18 13:52

@author: johannes
"""
import os
import setuptools


requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

NAME = 'sirena'
README = open('README.rst', 'r').read()

setuptools.setup(
    name=NAME,
    version="0.0.1",
    author="Johannes Johansson",
    author_email="johannes.johansson@smhi.se",
    description="Handle sea level data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JohannesSMHI/sirena",
    packages=setuptools.find_packages(),
    package_data={'sirena': [
        os.path.join('etc', '*.yaml'),
        os.path.join('etc', 'icons', '*.png'),
        os.path.join('etc', 'readers', '*.yaml'),
        os.path.join('etc', 'templates', '*.xlsx'),
        os.path.join('etc', 'writers', '*.yaml'),
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements,
)
