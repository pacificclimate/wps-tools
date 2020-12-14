import pytest
from pkg_resources import resource_filename
from collections import namedtuple
from wps_tools.utils import (
    is_opendap_url,
    get_filepaths,
    collect_output_files,
    build_meta_link,
    copy_http_content,
    url_handler,
    get_package,
    load_rdata_to_python,
    save_python_to_rdata,
)
from wps_tools.testing import (
    local_path,
    url_path,
)
from netCDF4 import Dataset
from tempfile import NamedTemporaryFile
from wps_tools.testing import run_wps_process
from os import path, remove
from pywps.app.exceptions import ProcessError
from rpy2 import robjects

NCInput = namedtuple("NCInput", ["url", "file"])
NCInput.__new__.__defaults__ = ("", "")

nc_file = "gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"


@pytest.mark.online
@pytest.mark.parametrize(
    ("url"), [url_path(nc_file, "opendap"), local_path(nc_file),],
)
def test_is_opendap_url(url):
    if "docker" in url:
        assert is_opendap_url(url)  # Ensure function recognizes this is an opendap file
    else:
        assert not is_opendap_url(
            url
        )  # Ensure function recognizes this is not an opendap file


@pytest.mark.parametrize(
    ("nc_input"), [[NCInput(file=local_path(nc_file))]],
)
def test_get_filepaths_local(nc_input):
    paths = get_filepaths(nc_input)
    assert len(paths) == len(nc_input)
    for path in paths:
        assert nc_file in path


@pytest.mark.online
@pytest.mark.parametrize(
    ("nc_input"),
    [
        [NCInput(url=url_path(nc_file, "opendap"))],
        [NCInput(file=local_path(nc_file)), NCInput(url=url_path(nc_file, "opendap")),],
    ],
)
def test_get_filepaths_online(nc_input):
    for nc in nc_input:
        if nc.url != "":
            assert is_opendap_url(nc.url)

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


@pytest.mark.online
@pytest.mark.parametrize(
    ("http", "expected"),
    [
        (
            url_path(nc_file, "http"),
            resource_filename(
                __name__, "data/gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc"
            ),
        ),
    ],
)
def test_copy_http_content(http, expected):
    with NamedTemporaryFile(
        suffix=".nc", prefix="tmp_copy", dir="/tmp", delete=True
    ) as tmp_file:
        tmp_copy = copy_http_content(http, tmp_file)
        assert dir(Dataset(tmp_copy)) == dir(Dataset(expected))


@pytest.mark.online
@pytest.mark.parametrize(
    ("url_type", "url"),
    [("http", url_path(nc_file, "http")), ("opendap", url_path(nc_file, "opendap")),],
)
def test_url_handler(url_type, url):
    processed = url_handler("/tmp", url)
    if url_type == "http":
        assert path.exists(processed)
        remove(processed)
    elif url_type == "opendap":
        assert is_opendap_url(processed)


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


@pytest.mark.parametrize(
    ("package"), [("base"), ("utils")],
)
def test_get_package(package):
    pkg = get_package(package)
    assert pkg.__dict__["__rname__"] == package


@pytest.mark.parametrize("package", ["invalid_pkg"])
def test_get_package_err(package):
    with pytest.raises(ProcessError) as e:
        get_package(package)
        assert str(vars(e)["_excinfo"][1]) == f"R package, {package}, is not installed"


@pytest.mark.parametrize(
    ("r_file", "r_object_name"),
    [(resource_filename(__name__, "data/expected_gsl.rda"), "expected_gsl_vector")],
)
def test_load_rdata_to_python(r_file, r_object_name):
    r2py_object = load_rdata_to_python(r_file, r_object_name)
    assert "robjects" in str(type(r2py_object))

    robjects.r("rm(list=ls())")


@pytest.mark.parametrize(
    ("r_name", "py_var"), [("str_ex", "string"), ("int_ex", 300),],
)
def test_save_python_to_rdata(r_name, py_var):
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True
    ) as r_file:
        save_python_to_rdata(r_name, py_var, r_file.name)
        test_var = load_rdata_to_python(r_file.name, r_name)

    assert test_var[0] == py_var

    robjects.r("rm(list=ls())")
