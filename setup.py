import sys

from setuptools import setup, find_packages

__version__ = (0, 1, 0)

setup(
    name="wps_tools",
    description="A collection of modules used to help create wps processes",
    keywords="wps pywps wps_tools",
    version='.'.join(str(d) for d in __version__),
    url="https://github.com/pacificclimate/wps-tools",
    author="Eric Yvorchuk",
    author_email="eyvorchuk@uvic.ca",
    packages=find_packages(),
    package_data={
        'wps_tools': ["wps_tools/*.py"],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
