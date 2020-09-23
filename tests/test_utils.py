import pytest
from pkg_resources import resource_filename
from collections import namedtuple
from wps_tools.utils import (
    is_opendap_url,
    get_filepaths,
    collect_output_files,
    build_meta_link,
    copy_http_content,
)
from wps_tools.testing import (
    local_path,
    opendap_path,
)
from .processes.wps_test_process import TestProcess
from netCDF4 import Dataset

NCInput = namedtuple("NCInput", ["url", "file"])
NCInput.__new__.__defaults__ = ("", "")

nc_file = "gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"


@pytest.mark.online
@pytest.mark.parametrize(
    ("url"), [opendap_path(nc_file), local_path(nc_file),],
)
def test_is_opendap_url(url):
    if "docker" in url:
        assert is_opendap_url(url)  # Ensure function recognizes this is an opendap file
    else:
        assert not is_opendap_url(
            url
        )  # Ensure function recognizes this is not an opendap file


@pytest.mark.online
@pytest.mark.parametrize(
    ("nc_input"),
    [
        [NCInput(file=local_path(nc_file))],
        [NCInput(url=opendap_path(nc_file))],
        [NCInput(file=local_path(nc_file)), NCInput(url=opendap_path(nc_file))],
    ],
)
def test_get_filepaths(nc_input):
    for input in nc_input:
        if input.url != "":
            assert is_opendap_url(input.url)

    paths = get_filepaths(nc_input)
    assert len(paths) == len(nc_input)
    for path in paths:
        assert nc_file in path


@pytest.mark.parametrize(
    ("varname", "outdir"), [("tiny", resource_filename(__name__, "data"))]
)
def test_collect_output_files(varname, outdir):
    outfiles = collect_output_files(varname, outdir)
    assert len(outfiles) == 2
    assert set(outfiles) == set(["tiny_daily_prsn.nc", "tiny_daily_pr.nc"])


@pytest.mark.parametrize(
    ("outfiles", "expected"),
    [
        (
            ["tiny_daily_prsn.nc", "tiny_daily_pr.nc"],
            ['<file name="tiny_daily_prsn.nc">', '<file name="tiny_daily_pr.nc">'],
        )
    ],
)
def test_build_meta_link(outfiles, expected):
    xml = build_meta_link(
        varname="climo",
        desc="Climatology",
        outfiles=outfiles,
        outdir=resource_filename(__name__, "data"),
    )
    assert all([elem in xml for elem in expected])


@pytest.mark.parametrize(
    ("http", "expected"),
    [
        (
            "https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/fileServer/datasets/TestData/gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc",
            resource_filename(
                __name__, "data/gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"
            ),
        )
    ],
)
def test_copy_http_content(http, expected):
    tmp_copy = copy_http_content(http)
    assert dir(Dataset(tmp_copy)) == dir(Dataset(expected))
