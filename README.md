# wps-tools


## Overview

The Web Processing Services (WPS) at PCIC, known as birds, are developed and tested using many common functions. The `wps-tools` repository was created to store these functions in a single place, mitigating redundant code across the birds, and to simplify the creation and testing of new WPS processes. Currently, this repo is used as a Python package for the `thunderbird`, `osprey`, and `sandpiper` repositories and should be used for future birds.

## Structure

The respository's functions are divided across three modules in the `wps_tools` directory, and each function's use is described in their respective docstring.

### utils.py

These functions gather PyWPS inputs, build PyWPS outputs, and handle logging information within a process's class file and are thus mainly used in `wps_*.py` files.

### io.py

This module contains a collection of commonly used PyWPS inputs and outputs and are also mainly used in `wps_*.py` files. These include the logging level, a toggle for if a dry run of the process should be executed, a single output netcdf file or a metalink connecting multiple output files, and a single output text file or metalink connecting multiple output text files containing the information provided by a dry run.

### testing.py

These functions help run a bird's `pytest` suite and are thus mainly used in `test_*.py` files. They consist of constructing the absolute local and OPeNDAP paths for a given file, building the WPS test client, and running a given process.

## Installation and Usage as Package

While in a different repository, the `wps-tools` package can be installed by executing

```bash
pip install wps-tools -i https://pypi.pacifcclimate.org/simple
```

Afterwards, each function can be used in a `.py` file by importing it. For example, if one wishes to use the `log_handler` function from `utils.py`, they access it by writing

```python
from wps_tools.utils import log_handler
```

## Installation as GitHub Repository

Clone the repo onto the target machine. Python installation should be done in a python3 virtual environment and activated as follows:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt -i https://pypi.pacificclimate.org/simple
```

## Development

Once the repository is cloned and the required development packages are installed, one can add new functions or PyWPS i/o objects by writing them in one of the aforementioned three modules or a new one in the `wps_tools` directory. Each function should have a corresponding test in the `tests` directory.

### Testing

More Python packages are required to run the tests and they can be installed by executing

```bash
pip install -r test_requirements.txt
```

The entire test suite can then be run by executing

```bash
pytest
```

and one can specify desired test functions as optional arguments. For example, one can run `test_is_opendap_url` from `test_utils.py` by executing

```bash
pytest tests/test_utils.py::test_is_opendap_url
```

### Releasing

To create a versioned release:

1. Increment `__version__` in `setup`
2. Summarize the changes from the last release in `NEWS.md`
3. Commit these changes, then tag the release:

  ```bash
git add setup NEWS.md
git commit -m"Bump to version x.x.x"
git tag -a -m"x.x.x" x.x.x
git push --follow-tags
  ```
4. [Github Actions](https://github.com/pacificclimate/climate-explorer-data-prep/blob/i130-full-actions/.github/workflows/pypi-publish.yml) will automatically build and publish the package to our pypi server