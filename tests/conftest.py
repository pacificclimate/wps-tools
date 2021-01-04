import pytest
import re
from pywps import Process, LiteralInput, ComplexInput, LiteralOutput, FORMATS
from wps_tools.io import collect_args
from wps_tools.file_handling import build_meta_link
from pkg_resources import resource_filename
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
                "file1",
                "File 1",
                max_occurs=2,
                abstract="Path to a local or online input file",
                supported_formats=[FORMATS.NETCDF, FORMATS.DODS],
            ),
            ComplexInput(
                "file2",
                "File 2",
                max_occurs=2,
                abstract="Path to another local or online input file",
                supported_formats=[FORMATS.NETCDF, FORMATS.DODS],
            ),
            LiteralInput(
                "argc",
                "Argument count dictionary",
                max_occurs=1,
                abstract="Number of input arguments for each input",
                data_type="string",
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
        count_dict = eval(request.inputs["argc"][0].data)

        for input_ in collected.keys():
            assert len(collected[input_]) == count_dict[input_]

        collected_argc = sum([len(collected[k]) for k in collected.keys()])
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


@pytest.fixture
def metalinks():
    outfiles = ["test.txt", "expected_gsl.rda"]

    xml = build_meta_link(
        varname="climo",
        desc="Climatology",
        outfiles=outfiles,
        outdir=resource_filename(__name__, "data"),
    )

    file_ = re.compile(">(file://.*)<")
    file_names = file_.findall(xml)
    if file_names:
        yield file_names
