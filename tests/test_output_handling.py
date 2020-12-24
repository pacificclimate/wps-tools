import pytest
from netCDF4._netCDF4 import Dataset

from wps_tools.output_handling import (
    nc_to_dataset,
    json_to_dict,
    vector_to_dict,
    txt_to_string,
    get_available_robjects,
)
from wps_tools.testing import url_path, local_path


@pytest.mark.online
@pytest.mark.parametrize(
    ("url"),
    [
        (url_path("tiny_gcm_climos.nc", "http")),
        (url_path("gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc", "http")),
    ],
)
def test_nc_to_dataset(url):
    dataset = nc_to_dataset(url)

    assert isinstance(dataset, Dataset)
    assert len(dataset.dimensions) > 0


@pytest.mark.parametrize(
    ("url"), [local_path("gsl.json")],
)
def test_json_to_dict(url):
    output_dict = json_to_dict(url)

    assert isinstance(output_dict, dict)
    assert len(output_dict) > 0


@pytest.mark.parametrize(
    ("url", "vector_name"), [(local_path("expected_gsl.rda"), "expected_gsl_vector")],
)
def test_vector_to_dict(url, vector_name):
    output_dict = vector_to_dict(url, vector_name)

    assert isinstance(output_dict, dict)
    assert len(output_dict) > 0


@pytest.mark.online
@pytest.mark.parametrize(
    ("url"),
    [
        (url_path("FileDescription.txt", "http", "climate_explorer_data_prep")),
        (url_path("sample_pour.txt", "http", "climate_explorer_data_prep")),
    ],
)
def test_txt_to_string(url):
    output_str = txt_to_string(url)

    assert output_str is not None
    assert output_str != ""
    assert isinstance(output_str, str)


@pytest.mark.parametrize(
    ("url"), [(local_path("expected_gsl.rda")), (local_path("expected_days_data.rda"))]
)
def test_get_available_robjects(url):
    objects = get_available_robjects(url)

    assert len(objects) > 0
    for ob in objects:
        assert isinstance(ob, str)
