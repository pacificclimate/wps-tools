# wps-tools

## Overview

The Web Processing Services (WPS) at PCIC, known as birds, are developed and tested using many common functions. The `wps-tools` repository was created to store these functions in a single place, mitigating redundant code across the birds, and to simplify the creation and testing of new WPS processes. Currently, this package is used in all the PCIC birds:
  - [`thunderbird`](https://github.com/pacificclimate/thunderbird)
  - [`osprey`](https://github.com/pacificclimate/osprey)
  - [`sandpiper`](https://github.com/pacificclimate/sandpiper)
  - [`chickadee`](https://github.com/pacificclimate/chickadee)
  - [`quail`](https://github.com/pacificclimate/quail).

## Structure

### io.py

This module contains a collection of commonly used PyWPS inputs and outputs and are also mainly used in `wps_*.py` files.

### testing.py

These functions help run a bird's `pytest` suite and are thus mainly used in `test_*.py` files.

### utils.py

These functions gather PyWPS inputs, build PyWPS outputs, and handle logging information within a process's class file and are thus mainly used in `wps_*.py` files.

## Installation as GitHub Repository

Clone the repo onto the target machine. Python installation should be done in a python3 virtual environment and activated as follows:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install .
```
The general installation using `.` will leave out the `rpy2` requirement. This is done to reduce the dependency load on the birds, specifically with `R` installation. If you wish to use the `R` capabilities use the `.[r]` or `.[complete]` installation scenarios.

In total there are 3 different extra installations available:
 - `[complete]` - everything needed to use the full package
 - `[r]` - base requirements + those needed to run the `R` methods
 - `[test]` - everything needed for testing

## Installation and Usage as Package

While in a different repository, the `wps-tools` package can be installed by executing

```bash
pip install -i https://pypi.pacifcclimate.org/simple wps-tools[complete]
```

Afterwards, each function can be used in a `.py` file by importing it. For example, if one wishes to use the `log_handler` function from `utils.py`, they access it by writing

```python
from wps_tools.utils import log_handler
```

## Development

Once the repository is cloned and the required development packages are installed, one can add new functions or PyWPS i/o objects by writing them in one of the aforementioned three modules or a new one in the `wps_tools` directory. Each function should have a corresponding test in the `tests` directory.

### Testing

More Python packages are required to run the tests and they can be installed by executing

```bash
pip install .[test]
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
4. [Github Actions](https://github.com/pacificclimate/wps-tools/blob/i16-update-documentation/.github/workflows/pypi-publish.yml) will automatically build and publish the package to our pypi server
