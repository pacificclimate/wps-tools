import pytest
import os

from wps_tools.testing import (
    local_path,
    opendap_path,
    run_wps_process,
    get_target_url,
)
from .test_processes.wps_test_process import TestProcess

nc_file = "gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"


@pytest.mark.parametrize(("nc_file"), [nc_file])
def test_local_path(nc_file):
    assert f"tests/data/{nc_file}" in local_path(nc_file)


@pytest.mark.online
@pytest.mark.parametrize(("nc_file"), [nc_file])
def test_opendap_path(nc_file):
    assert "/datasets/storage/data/projects/comp_support/" in opendap_path(
        nc_file
    ) and nc_file in opendap_path(nc_file)


@pytest.mark.parametrize(("string"), ["Hello"])
def test_run_wps_process(string):
    params = f"string={string}"
    run_wps_process(TestProcess(), params)


@pytest.mark.parametrize(
    "bird", [("thunderbird"), ("sandpiper"), ("osprey"), ("chickadee"),]
)
@pytest.mark.parametrize("expected", ["http://localhost:5000/wps"])
def test_get_target_url_local(mock_local_url, bird, expected):
    assert get_target_url(bird) == expected


@pytest.mark.parametrize(
    "bird", [("thunderbird"), ("sandpiper"), ("osprey"), ("chickadee"),]
)
@pytest.mark.parametrize("expected", ["http://docker-dev03.pcic.uvic.ca/somebird"])
def test_get_target_url_dev(mock_dev_url, bird, expected):
    assert get_target_url(bird) == expected


@pytest.mark.parametrize(
    "bird", [("thunderbird"), ("sandpiper"), ("osprey"), ("chickadee"),]
)
def test_get_target_url(bird):
    assert bird in get_target_url(bird)
