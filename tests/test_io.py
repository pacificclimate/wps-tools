import pytest
from wps_tools.testing import (
    local_path,
    url_path,
)
from wps_tools.testing import run_wps_process


def run_args_collection(wps_test_process_multi_input, file, csv, argc):
    params = (
        ";".join([f"file={nc}" for nc in file])
        + f';csv_input="{csv}"'
        + f";argc={argc};"
    )
    run_wps_process(wps_test_process_multi_input, params)


@pytest.mark.parametrize(
    ("file", "argc"),
    [
        (
            [local_path("tiny_daily_pr.nc"), local_path("tiny_daily_prsn.nc"),],
            {"file": 2, "csv_input": 1, "argc": 1},
        )
    ],
)
def test_collect_args_local(wps_test_process_multi_input, file, csv_data, argc):
    run_args_collection(wps_test_process_multi_input, file, f"{csv_data}", argc)


@pytest.mark.online
@pytest.mark.parametrize(
    ("file", "csv", "argc"),
    [
        (
            [
                url_path(
                    "sample.rvic.prm.COLUMBIA.20180516.nc",
                    "http",
                    "climate_explorer_data_prep",
                )
            ],
            [
                "https://raw.githubusercontent.com/pacificclimate/sandpiper/master/tests/data/tiny_rules.csv",
            ],
            {"file": 1, "csv_input": 1, "argc": 1},
        )
    ],
)
def test_collect_args_online(wps_test_process_multi_input, file, csv, argc):
    run_args_collection(wps_test_process_multi_input, file, csv, argc)
