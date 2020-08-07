import pytest

from wps_tools.testing import (
    local_path,
    opendap_path,
    run_wps_process,
)
from .processes.wps_test_process import TestProcess

nc_file = "gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"


@pytest.mark.parametrize(("nc_file"), [nc_file])
def test_local_path(nc_file):
    assert f"tests/data/{nc_file}" in local_path(nc_file)


@pytest.mark.online
@pytest.mark.parametrize(("nc_file"), [nc_file])
def test_opendap_path(nc_file):
    assert f"datasets/TestData/{nc_file}" in opendap_path(nc_file)


@pytest.mark.parametrize(("string"), ["Hello"])
def test_run_wps_process(string):
    params = f"string={string}"
    run_wps_process(TestProcess(), params)
