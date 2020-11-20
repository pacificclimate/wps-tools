from pywps import Process, LiteralInput, ComplexInput, LiteralOutput, FORMATS
from wps_tools.utils import collect_args
import logging


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
