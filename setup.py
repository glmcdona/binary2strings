#! /usr/bin/0env python3
# Templated from https://github.com/pybind/python_example
import sys
import os
from glob import glob

from pybind11 import get_cmake_dir
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, Extension, find_packages

__version__ = "0.1.13"

ext_modules = [
    Pybind11Extension("binary2strings",
        sorted(glob("src/*.cpp")),  # Sort source files for reproducibility
        define_macros = [('VERSION_INFO', __version__)],
        include_dirs = ["src"],
        ),
]

# Note to self to build and upload skip existing:
#   Delete dist/ and build/
#   python setup.py sdist bdist_wheel
#   twine upload dist/* --skip-existing
#     Get token from https://pypi.org/manage/account/token/
#     Use username __token__
#     Use password from token
#     Delete token after use
#with open("README.md", "r") as fh:
#    long_description = fh.read()
long_description = "Fast string extraction from binary buffers."
setup(
    name='binary2strings',
    version=__version__,
    author='Geoff McDonald',
    author_email='glmcdona@gmail.com',
    url='https://github.com/glmcdona/binary2strings',
    license='MIT',
    description='Fast string extraction from binary buffers.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    test_suite='tests',
    zip_safe=False,
    python_requires=">=3.7",
)