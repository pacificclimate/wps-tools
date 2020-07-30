import pytest
from pkg_resources import resource_filename
from wps_tools.utils import (
    is_opendap_url,
    get_filepaths,
    collect_output_files,
    build_meta_link,
)
from wps_tools.testing import (
    local_path,
    opendap_path,
    run_wps_process,
)
from processes.wps_say_hello import SayHello

nc_file = "gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"


class NCInput:  # For testing 'get_filepaths'
    def __init__(self, url="", file=""):
        self.url = url
        self.file = file


# Test 'testing' functions
def test_local_path():
    assert f"tests/data/{nc_file}" in local_path(nc_file)


def test_opendap_path():
    assert f"datasets/TestData/{nc_file}" in opendap_path(nc_file)


def test_run_wps_process():
    params = "name=PCIC"
    run_wps_process(SayHello(), params)


# Test 'utils' functions
@pytest.mark.online
@pytest.mark.parametrize(
    ("url"), [opendap_path(nc_file), local_path(nc_file),],
)
def test_is_opendap_url(url):
    if "docker" in url:
        assert is_opendap_url(url)
    else:
        assert not is_opendap_url(url)


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


@pytest.mark.parametrize(("varname"), ["tiny"])
@pytest.mark.parametrize(("outdir"), [resource_filename(__name__, "data")])
def test_collect_output_files(varname, outdir):
    outfiles = collect_output_files(varname, outdir)
    assert len(outfiles) == 2
    assert outfiles == ["tiny_daily_prsn.nc", "tiny_daily_pr.nc"]


@pytest.mark.parametrize(("outfiles"), [["tiny_daily_prsn.nc", "tiny_daily_pr.nc"]])
def test_build_meta_link(outfiles):
    xml = build_meta_link(
        varname="climo",
        desc="Climatology",
        outfiles=outfiles,
        outdir=resource_filename(__name__, "data"),
    )
    assert (
        '<file name="tiny_daily_prsn.nc">' in xml
        and '<file name="tiny_daily_pr.nc">' in xml
    )
