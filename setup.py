import sys
from setuptools import setup

__version__ = (1, 2, 0)

try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    warn("Could not import sphinx. You won't be able to build the docs")

reqs = [line.strip() for line in open("requirements.txt")]

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
    install_requires=reqs,
    cmdclass={"build_sphinx": BuildDoc},
    command_options={
        "build_sphinx": {
            "project": ("setup.py", "wps_tools"),
            "version": ("setup.py", ".".join(str(d) for d in __version__)),
            "source_dir": ("setup.py", "doc/source"),
        }
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
