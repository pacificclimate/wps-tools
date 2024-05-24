import pytest
from netCDF4._netCDF4 import Dataset

from wps_tools.output_handling import (
    nc_to_dataset,
    json_to_dict,
    txt_to_string,
    auto_construct_outputs,
    get_metalink_content,
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
    ("url"),
    [local_path("gsl.json")],
)
def test_json_to_dict(url):
    output_dict = json_to_dict(url)

    assert isinstance(output_dict, dict)
    assert len(output_dict) > 0


def txt_to_string_test(url):
    output_str = txt_to_string(url)

    assert output_str is not None
    assert output_str != ""
    assert isinstance(output_str, str)


@pytest.mark.online
@pytest.mark.parametrize(
    ("url"),
    [
        (url_path("FileDescription.txt", "http", "climate_explorer_data_prep")),
        (url_path("sample_pour.txt", "http", "climate_explorer_data_prep")),
    ],
)
def test_txt_to_string_online(url):
    txt_to_string_test(url)


def test_txt_to_string_local(txt_file):
    txt_to_string_test(f"file://{txt_file.name}")
    txt_file.close()


def auto_construct_outputs_test(outputs, expected_types):
    process_outputs = auto_construct_outputs(outputs)
    for i in range(len(process_outputs)):
        assert type(process_outputs[i]) == expected_types[i]


@pytest.mark.online
@pytest.mark.parametrize(
    ("outputs", "expected_types"),
    [
        (
            [
                url_path("FileDescription.txt", "http", "climate_explorer_data_prep"),
                url_path("tiny_gcm_climos.nc", "http"),
            ],
            [str, Dataset],
        )
    ],
)
def test_auto_construct_outputs_online(outputs, expected_types):
    auto_construct_outputs_test(outputs, expected_types)


@pytest.mark.parametrize(
    ("outputs", "expected_types"),
    [
        (
            ["test string"],
            [str, str],
        )
    ],
)
def test_auto_construct_outputs_local(txt_file, outputs, expected_types):
    outputs.append(f"file://{txt_file.name}")
    auto_construct_outputs_test(outputs, expected_types)
    txt_file.close()


@pytest.mark.parametrize(
    ("output"),
    ["https://test_metalinks.meta4"],
)
def test_get_metalink_content(mock_metalink, output):
    for file_ in get_metalink_content(output):
        assert file_.endswith((".json", ".nc"))
