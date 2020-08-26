from pkg_resources import resource_filename
from pywps import Service
from pywps.app.basic import get_xpath_ns
from pywps.tests import WpsClient, WpsTestResponse, assert_response_success

VERSION = "1.0.0"
xpath_ns = get_xpath_ns(VERSION)


class WpsTestClient(WpsClient):
    def get(self, *args, **kwargs):
        """Build get request to run WPS process."""
        query = "?"
        for key, value in kwargs.items():
            query += "{0}={1}&".format(key, value)
        return super(WpsTestClient, self).get(query)


def local_path(file_name):
    """Return absolute path of file in tests/data directory.
    Parameters:
        file_name (str): File name
    """
    return f"file:///{resource_filename('tests', 'data/' + file_name)}"


def opendap_path(file_name):
    """Return OpenDAP url for file.
    Parameters:
        file_name (str): File name
    """
    return f"https://docker-dev03.pcic.uvic.ca/twitcher/ows/proxy/thredds/dodsC/datasets/TestData/{file_name}"


def client_for(service):
    """Create WPS client to run process.
    Parameters:
        service (Service): Service for WPS process
    """
    return WpsTestClient(service, WpsTestResponse)


def run_wps_process(process, params):
    """Run WPS process and ensure that execution is successful.
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
