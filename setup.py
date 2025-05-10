# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from setuptools import setup
import coinprecio

with open("README.md") as f:
    doc = f.read()

setup(
    name="coinprecio",
    version=coinprecio.__version__,
    description="Crypto API client for fetching market price data via multiple backends.",
    long_description=doc,
    long_description_content_type="text/markdown",
    author=coinprecio.__author__,
    author_email=coinprecio.__author_email__,
    url="https://github.com/joetor5/coinprecio",
    license=coinprecio.__license__,
    platforms="any",
    install_requires=[
        "requests==2.32.3"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
