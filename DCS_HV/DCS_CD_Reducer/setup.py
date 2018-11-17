#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 17:25:06 2018

@author: Luca Clissa
"""

import setuptools

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open("/home/luca/Desktop/Dottorato/Ricerca/Conditions_Data/DCS_HV/DCS_CD_Reducer/README.md", "r") as rmfile:
    long_description = rmfile.read()

setuptools.setup(
    name = "dcs_cd_reducer",
    version = "0.1.0",
    author = "Luca Clissa",
    author_email = "luca.clissa2@unibo.it",
    description = ("Package to replicate DCS Condition's Data from ATLAS experiment at CERN in a reduced-size, fast-access manner by means of a parametric function"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = "example documentation tutorial",
    license = "GNUv3 GPL",
    #license = "Apache Software License",
    #url = "http://packages.python.org/an_example_pypi_project", #GitHub link to project
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Alpha",
        #"Topic :: Utilities",
        "License :: OSI Approved :: GNUv3 GPL",
        #"License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)