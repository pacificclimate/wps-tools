import pytest
import requests
from tempfile import NamedTemporaryFile
from pywps import Process, LiteralInput, ComplexInput, LiteralOutput, FORMATS, Format
from wps_tools.io import collect_args
from wps_tools.file_handling import build_meta_link
from pkg_resources import resource_filename
import logging


@pytest.fixture
def mock_local_url(monkeypatch):
    monkeypatch.setenv("LOCAL_URL", "http://localhost:5000/wps")


@pytest.fixture
def mock_dev_url(monkeypatch):
    monkeypatch.setenv("DEV_URL", "http://marble-dev01.pcic.uvic.ca/somebird")


LOGGER = logging.getLogger("PYWPS")


class TestProcessMultiInput(Process):
    """A simple wps process for test_collect_args in test_utils.py"""

    def __init__(self):
        inputs = [
            ComplexInput(
                "file",
                "File",
                max_occurs=2,
                abstract="Path to a local or online nc file",
                supported_formats=[FORMATS.NETCDF, FORMATS.DODS],
            ),
            ComplexInput(
                "csv_input",
                "CSV",
                max_occurs=1,
                abstract="CSV document",
                supported_formats=[Format("text/csv", extension=".csv"), FORMATS.TEXT],
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

        super(TestProcessMultiInput, self).__init__(
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
        collected = collect_args(request.inputs, self.workdir)
        count_dict = eval(request.inputs["argc"][0].data)

        collected_argc = 0
        for input_ in collected.keys():
            if isinstance(collected[input_], list):
                collected_argc += len(collected[input_])
                assert len(collected[input_]) == count_dict[input_]

            else:
                collected_argc += 1
                assert type(collected[input_]) != list

        response.outputs["collected_argc"].data = collected_argc
        return response


@pytest.fixture
def wps_test_process_multi_input(monkeypatch):
    return TestProcessMultiInput()


class TestProcess(Process):
    """A simple wps process. Outputs the input string."""

    def __init__(self):
        self.status_percentage_steps = {  # Used to test 'log_handler'
            "start": 0,
            "complete": 100,
        }
        inputs = [
            LiteralInput(
                "string",
                "String",
                abstract="Enter string.",
                data_type="string",
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
def txt_file():
    txt = NamedTemporaryFile(suffix=".txt", prefix="test_txt", dir="/tmp", delete=True)
    txt.write(b"Test txt file")
    txt.seek(0)

    yield txt


class MockResponse:
    def __init__(self, content):
        self.content = content.encode()

    def meta4(self):
        return self.content


def mock_metalink_respose(*args, **kwargs):
    outfiles = ["gsl.json", "tiny_daily_pr.nc"]
    metalink = build_meta_link(
        varname="climo",
        desc="Climatology",
        outfiles=outfiles,
        outdir=resource_filename(__name__, "data"),
    )

    if args[0] == "https://test_metalinks.meta4":
        return MockResponse(metalink)


@pytest.fixture
def mock_metalink(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_metalink_respose)


@pytest.fixture
def csv_data():
    return open(resource_filename("tests", "data/tiny_rules.csv")).read()
