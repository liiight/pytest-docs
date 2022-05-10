#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-docs",
    version="0.2.0",
    author="Or Carmi",
    author_email="or.carmi82@gmail.com",
    maintainer="Or Carmi",
    maintainer_email="or.carmi82@gmail.com",
    license="MIT",
    url="https://github.com/liiight/pytest-docs",
    description="Documentation tool for pytest",
    long_description=read("README.rst"),
    python_requires=">=3.4",
    install_requires=["pytest>=3.5.0"],
    packages=find_packages(exclude=["pytest_docs.tests"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["docs = pytest_docs.plugin"]},
)
