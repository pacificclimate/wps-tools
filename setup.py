import sys

from setuptools import setup

__version__ = (0, 0, 1)

setup(
    name="wps_tools",
    description="A collection of modules used to help create wps processes",
    keywords="wps pywps wps_tools",
    version='.'.join(str(d) for d in __version__),
    url="https://github.com/pacificclimate/wps-tools",
    author="Eric Yvorchuk",
    author_email="eyvorchuk@uvic.ca",
    packages=["wps_tools"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
