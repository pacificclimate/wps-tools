import pytest
import logging
from pkg_resources import resource_filename
from wps_tools.utils import (
    is_opendap_url,
    get_filepaths,
    collect_output_files,
    build_meta_link,
    log_handler,
)
from wps_tools.testing import (
    local_path,
    opendap_path,
    run_wps_process,
)
from .processes.wps_test_process import TestProcess
from .conftest import NCInput, Response

nc_file = "gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"


# Test 'testing' functions


@pytest.mark.parametrize(("nc_file"), [nc_file])
def test_local_path(nc_file):
    assert f"tests/data/{nc_file}" in local_path(nc_file)


@pytest.mark.online
@pytest.mark.parametrize(("nc_file"), [nc_file])
def test_opendap_path(nc_file):
    assert f"datasets/TestData/{nc_file}" in opendap_path(nc_file)


@pytest.mark.parametrize(("name"), ["PCIC"])
def test_run_wps_process(name):
    params = f"name={name}"
    run_wps_process(TestProcess(), params)


# Test 'utils' functions
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


@pytest.mark.parametrize(("varname"), ["tiny"])
@pytest.mark.parametrize(("outdir"), [resource_filename(__name__, "data")])
def test_collect_output_files(varname, outdir):
    outfiles = collect_output_files(varname, outdir)
    assert len(outfiles) == 2
    assert set(outfiles) == set(["tiny_daily_prsn.nc", "tiny_daily_pr.nc"])


@pytest.mark.parametrize(("outfiles"), [["tiny_daily_prsn.nc", "tiny_daily_pr.nc"]])
@pytest.mark.parametrize(
    ("expected"),
    [['<file name="tiny_daily_prsn.nc">', '<file name="tiny_daily_pr.nc">']],
)
def test_build_meta_link(outfiles, expected):
    xml = build_meta_link(
        varname="climo",
        desc="Climatology",
        outfiles=outfiles,
        outdir=resource_filename(__name__, "data"),
    )
    assert all([elem in xml for elem in expected])


@pytest.mark.parametrize(("message"), ["Process completed"])
@pytest.mark.parametrize(("process_step"), ["complete"])
def test_log_handler(message, process_step, caplog):
    response = Response()
    caplog.set_level(logging.INFO, logger="PYWPS")
    log_handler(TestProcess(), response, message=message, process_step=process_step)
    assert response.message == message
    assert (
        response.status_percentage
        == TestProcess().status_percentage_steps[process_step]
    )
    # for record in caplog.records:
    #    assert record.levelno == "INFO"
    # assert message in caplog.text
