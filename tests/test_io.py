import pytest
from wps_tools.testing import (
    local_path,
    url_path,
)
from wps_tools.testing import run_wps_process


def collect_args_test(wps_test_collect_args, file1, file2, argc):
    params = (
        ";".join(
            [f"file1={nc}" for nc in file1] + [f"file2={file_}" for file_ in file2]
        )
        + f";argc={argc};"
    )
    run_wps_process(wps_test_collect_args, params)


@pytest.mark.parametrize(
    ("file1", "file2", "argc"),
    [
        (
            [local_path("tiny_daily_pr.nc"), local_path("tiny_daily_prsn.nc"),],
            [local_path("gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc")],
            {"file1": 2, "file2": 1, "argc": 1},
        )
    ],
)
def test_collect_args_local(wps_test_collect_args, file1, file2, argc):
    collect_args_test(wps_test_collect_args, file1, file2, argc)


@pytest.mark.online
@pytest.mark.parametrize(
    ("file1", "file2", "argc"),
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
                url_path("tiny_daily_pr.nc", "opendap"),
                url_path("tiny_daily_prsn", "opendap"),
            ],
            {"file1": 1, "file2": 2, "argc": 1},
        )
    ],
)
def test_collect_args_online(wps_test_collect_args, file1, file2, argc):
    collect_args_test(wps_test_collect_args, file1, file2, argc)
