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
)
from .test_processes.wps_generate_climos import GenerateClimos

test_local_file = local_path("gdd_annual_CanESM2_rcp85_r1i1p1_1951-2100.nc")


def setup_wps_process():
    params = (
        f"netcdf=@xlink:href={test_local_file};"
        "operation=mean;"
        "climo=6190;"
        "resolutions=yearly;"
        "convert_longitudes=True;"
        "split_vars=True;"
        "split_intervals=True;"
        "dry_run=False;"
    )
    return params


@pytest.mark.online
@pytest.mark.parametrize(
    ("url"),
    [
        "http://docker-dev03.pcic.uvic.ca:8083/twitcher/ows/proxy/thredds/dodsC/datasets/TestData/tiny_hydromodel_gcm_climos.nc",
        test_local_file,
    ],
)
def test_is_opendap_url(url):
    if "docker" in url:
        assert is_opendap_url(url)
    else:
        assert not is_opendap_url(url)


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
