import pytest
from pywps import Process, LiteralInput, ComplexInput, LiteralOutput, FORMATS
from wps_tools.utils import collect_args
import logging


@pytest.fixture
def mock_local_url(monkeypatch):
    monkeypatch.setenv("LOCAL_URL", "http://localhost:5000/wps")


@pytest.fixture
def mock_dev_url(monkeypatch):
    monkeypatch.setenv("DEV_URL", "http://docker-dev03.pcic.uvic.ca/somebird")


LOGGER = logging.getLogger("PYWPS")


class TestCollectArgs(Process):
    """A simple wps process for test_collect_args in test_utils.py"""

    def __init__(self):
        inputs = [
            ComplexInput(
                "local_file",
                "Local file",
                max_occurs=5,
                abstract="Path to the local input file",
                supported_formats=[FORMATS.NETCDF],
            ),
            ComplexInput(
                "opendap_url",
                "OPeNDAP URL",
                max_occurs=5,
                abstract="URL to the opendap input file",
                supported_formats=[FORMATS.DODS],
            ),
            LiteralInput(
                "argc",
                "Argument count",
                max_occurs=5,
                abstract="Number of input arguments",
                data_type="integer",
            ),
        ]
        outputs = [
            LiteralOutput(
                "collected_argc",
                "Collected argument count",
                abstract="Number of collected arguments",
                data_type="integer",
            ),
        ]

        super(TestCollectArgs, self).__init__(
            self._handler,
            identifier="test_collect_args",
            title="Test collect_args",
            abstract="A simple process that tests collect_args.",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
        )

    def _handler(self, request, response):
        collected = collect_args(request, self.workdir)
        collected_argc = sum([len(collected[k]) for k in collected.keys()])

        assert collected_argc == request.inputs["argc"][0].data

        response.outputs["collected_argc"].data = collected_argc
        return response


@pytest.fixture
def wps_test_collect_args(monkeypatch):
    return TestCollectArgs()


class TestProcess(Process):
    """A simple wps process. Outputs the input string."""

    def __init__(self):
        self.status_percentage_steps = {  # Used to test 'log_handler'
            "start": 0,
            "complete": 100,
        }
        inputs = [
            LiteralInput(
                "string", "String", abstract="Enter string.", data_type="string",
            )
        ]
        outputs = [
            LiteralOutput(
                "output",
                "Output response",
                abstract="Outputs string entered.",
                data_type="string",
            )
        ]

        super(TestProcess, self).__init__(
            self._handler,
            identifier="test_process",
            title="Test Process",
            abstract="A simple process that returns the string that was inputted.",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
        )

    @staticmethod
    def _handler(request, response):
        LOGGER.info("Begin test process")
        response.outputs["output"].data = request.inputs["string"][0].data
        return response


@pytest.fixture
def wps_test_process(monkeypatch):
    return TestProcess()
