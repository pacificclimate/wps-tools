from pywps import Process, LiteralInput, LiteralOutput, UOM
from pywps.app.Common import Metadata

import logging

LOGGER = logging.getLogger("PYWPS")


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

        super(SayHello, self).__init__(
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
        response.outputs["output"].data = request.inputs["name"][0].data
        return response
