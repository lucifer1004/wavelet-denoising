#!/usr/bin/env python
"""Setup script for building prosail's python bindings"""
import os
import codecs
import re
from os import path
from setuptools import setup

# Global variables for this extension:
name = "wldenoise"  # name of the generated python extension (.so)
description = "Wavelet denoising functions"
long_description = "Wavelet denoising functions, including DWT, SWT, LWT, SLWT"

this_directory = path.abspath(path.dirname(__file__))


def read(filename):
    with open(os.path.join(this_directory, filename), "rb") as f:
        return f.read().decode("utf-8")


if os.path.exists("README.md"):
    long_description = read("README.md")


def read(*parts):
    with codecs.open(os.path.join(this_directory, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


author = "Gabriel Wu"
author_email = "wuzihua@pku.edu.cn"
url = "https://github.com/lucifer1004/wldenoise"
classifiers = [
    'Development Status :: 3',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries :: Python Modules',
    "Topic :: Scientific/Engineering :: Signal Processing",
    'Intended Audience :: Science/Research',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'Environment :: Console'
]


setup(
    name=name,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=author,
    url=url,
    author_email=author_email,
    classifiers=classifiers,
    package_data={"wldenoise": ["*.txt"]},
    install_requires=[
        "numpy",
        "pywt",
    ],
    version=find_version("wldenoise", "__init__.py"),
    packages=["wldenoise"],
    zip_safe=False  # Apparently needed for conda
)
