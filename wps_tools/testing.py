from pkg_resources import resource_filename
from pywps import Service
from pywps.app.basic import get_xpath_ns
from pywps.tests import WpsClient, WpsTestResponse, assert_response_success
import os

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
    return f"file:///{resource_filename('tests', 'data/' + sub_filepath)}"


def opendap_path(sub_filepath):
    """Return OpenDAP url for a file located under /storage/data

    Parameters:
        sub_filepath (str): Sub filepath

    Returns:
        str: OpenDAP url
    """
    return f"https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/storage/data/{sub_filepath}"


def http_server_path(sub_filepath):
    """Return HTTPServer url for a file located under /storage/data

    Parameters:
        sub_filepath (str): Sub filepath

    Returns:
        str: HTTPServer url
    """
    return f"https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/fileServer/datasets/storage/data/{sub_filepath}"


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

    assert_response_success(resp)


def get_target_url(bird):
    """Given a bird, determine which url to target for notebooks

    "DEV" and "LOCAL" urls may be targeted by the Makefile testing procedures.
    If neither of those environment variables are set, the default docker url will be used.
    """
    for url in [os.getenv("DEV_URL"), os.getenv("LOCAL_URL")]:
        if url:
            return url

    return f"https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/{bird}/wps"
