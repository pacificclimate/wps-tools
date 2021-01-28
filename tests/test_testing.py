import pytest

from wps_tools.testing import (
    local_path,
    url_path,
    run_wps_process,
    get_target_url,
)

nc_file = "gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"


@pytest.mark.parametrize(("nc_file"), [nc_file])
def test_local_path(nc_file):
    assert f"tests/data/{nc_file}" in local_path(nc_file)


@pytest.mark.online
@pytest.mark.parametrize(
    ("nc_file", "url_type", "sub_dir"),
    [
        (nc_file, "opendap", "daccs"),
        (nc_file, "http", "daccs"),
        (nc_file, "opendap", "climate_explorer_data_prep"),
    ],
)
def test_url_path(nc_file, url_type, sub_dir):
    if url_type == "opendap":
        assert (
            f"dodsC/datasets/storage/data/projects/comp_support/{sub_dir}"
            in url_path(nc_file, url_type, sub_dir)
        )
    elif url_type == "http":
        assert (
            f"fileServer/datasets/storage/data/projects/comp_support/{sub_dir}"
            in url_path(nc_file, url_type, sub_dir)
        )


@pytest.mark.parametrize(("string"), ["Hello"])
def test_run_wps_process(wps_test_process, string):
    params = f"string={string}"
    run_wps_process(wps_test_process, params)


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
