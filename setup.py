import sys
from setuptools import setup


__version__ = (1, 2, 0)


# Detail different installation scenarios
extras_require = {
    "r": ["rpy2 == 3.3.6"],
}
extras_require["complete"] = {
    requirements for scenario in extras_require.values() for requirements in scenario
}
extras_require["test"] = ["pytest == 5.4.3", "black == 19.10b0"]

# Main installation requirements
install_requires = [
    "pywps >= 4.2.6",
    "nchelpers == 5.5.7",
    "netCDF4 >= 1.5.4",
    "beautifulsoup4 == 4.9.3",
]

setup(
    name="wps_tools",
    description="A collection of modules used to help create wps processes",
    keywords="wps pywps wps_tools",
    version=".".join(str(d) for d in __version__),
    url="https://github.com/pacificclimate/wps-tools",
    author="Eric Yvorchuk",
    author_email="eyvorchuk@uvic.ca",
    packages=["wps_tools"],
    package_data={
        "wps-tools": ["tests/data/*.nc", "tests/processes/*.py"],
        "tests": ["data/*.nc", "processes/*.py"],
    },
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
