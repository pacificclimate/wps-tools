import os
import io
import pytest
from importlib.resources import files
from pywps import Service
from pywps.app.basic import get_xpath_ns
from pywps.tests import WpsClient, WpsTestResponse

VERSION = "1.0.0"
xpath_ns = get_xpath_ns(VERSION)


class WpsTestClient(WpsClient):
    """WPS client for testing processes"""

    def get(self, **kwargs):
        """Build and send get request to run WPS process

        Each parameter given by **kwargs is used as an element in a
        get request query. Once the query is constructed, it is used as a
        parameter for the WpsClient's get method.

        Parameters:
            **kwargs: key-value pairs used as query arguments

        Returns:
            WpsTestResponse: Response object from process execution
        """
        query = "?"
        for key, value in kwargs.items():
            query += "{0}={1}&".format(key, value)
        return super(WpsTestClient, self).get(query)


def local_path(sub_filepath):
    """Return absolute path of file located under tests/data directory

    Parameters:
        sub_filepath (str): Sub filepath

    Returns:
        str: Absolute local file path
    """
    data_dir = files("tests") / "data"
    full_path = (data_dir / sub_filepath).resolve()
    return f"file://{full_path}"


def url_path(sub_filepath, url_type, sub_dir="daccs"):
    """Return url for a file located under /storage/data

    Parameters:
        sub_filepath (str): Sub filepath
        url_type (str):  opendap/http
        sub_dir (str): The file must be in one of these subdirectories
                       daccs/climate_explorer_data_prep

    Returns:
        str: Full url
    """
    if url_type == "opendap":
        identifier = "dodsC"
    elif url_type == "http":
        identifier = "fileServer"
    else:
        raise ValueError(f'Invalid url_type argument "{url_type}"')

    if sub_dir == "daccs":
        path = "daccs/test-data"
    elif sub_dir == "climate_explorer_data_prep":
        path = "climate_explorer_data_prep/hydro/sample_data/set4"
    else:
        raise ValueError(
            f'Invalid sub directory "{sub_dir}": must be one of "daccs" or "climate_explorer_data_prep"'
        )

    return f"https://marble-dev01.pcic.uvic.ca/twitcher/ows/proxy/thredds/{identifier}/datasets/storage/data/projects/comp_support/{path}/{sub_filepath}"


def client_for(service):
    """Create WPS client to run process

    Parameters:
        service (Service): Service for WPS process

    Returns:
        WpsTestClient: WPS client for running process in service
    """
    return WpsTestClient(service, WpsTestResponse)


def run_wps_process(process, params):
    """Run WPS process and ensure that execution is successful

    A WPS test client is created to build the get request to run the
    specified process, and the parameters are used as inputs to this request.
    After execution, the status code of the response is checked to ensure success.

    Parameters:
        process (Process): Process to run
        params (str): Process parameters
    """
    client = client_for(Service(processes=[process]))
    datainputs = params
    resp = client.get(
        service="wps",
        request="Execute",
        version="1.0.0",
        identifier=process.identifier,
        datainputs=datainputs,
    )
    return resp


def process_err_test(process, datainputs):
    """Runs a WPS process and checks that it fails with a ProcessFailed response.

    Parameters:
    process (Process): Process name to run
        (eg/ 'ProcessName' NOT 'ProcessName()')
    datainputs (str): Process parameters
    """
    resp = run_wps_process(process(), datainputs)
    # Check that the response contains a ProcessFailed element
    failed = resp.xpath("/wps:ExecuteResponse/wps:Status/wps:ProcessFailed")
    assert len(failed) == 1, f"Expected ProcessFailed, got {resp.response}"


def get_target_url(bird):
    """Given a bird, determine which url to target for notebooks

    "DEV" and "LOCAL" urls may be targeted by the Makefile testing procedures.
    If neither of those environment variables are set, the default docker url will be used.
    """
    for url in [os.getenv("DEV_URL"), os.getenv("LOCAL_URL")]:
        if url:
            return url

    return f"https://marble-dev01.pcic.uvic.ca/twitcher/ows/proxy/{bird}/wps"
