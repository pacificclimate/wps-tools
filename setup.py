import sys

from setuptools import setup

__author__ = "Eric Yvorchuk"
__email__ = "eyvorchuk@uvic.ca"
__version__ = "0.1.0"

setup(
    name="wps_tools",
    description="A collection of modules used to help create wps processes",
    keywords="wps pywps wps_tools",
    version=__version__,
    url="https://github.com/pacificclimate/wps-tools",
    author=__author__,
    author_email=__email__,
    packages=["wps_tools"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
