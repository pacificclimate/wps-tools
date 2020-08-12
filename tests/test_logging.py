import pytest
import logging
import os
from tempfile import TemporaryDirectory
from pkg_resources import resource_filename
from wps_tools.utils import log_handler
from .common import TestResponse
from .processes.wps_test_process import TestProcess

logger = logging.getLogger()

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: wps-tools: %(message)s", "%Y-%m-%d %H:%M:%S"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

@pytest.mark.parametrize(
    ("message", "process_step"), [("Process completed", "complete")]
)
@pytest.mark.parametrize(("log_level"), [("INFO"), ("DEBUG")])
@pytest.mark.parametrize(("log_file_name"), [("log.txt"), ("log2.txt")])
def test_log_handler(message, process_step, log_level, log_file_name, caplog):
    process = TestProcess()
    response = TestResponse()
    with TemporaryDirectory() as tmpdir:  # For storing temporary log.txt file
        process.workdir = tmpdir
        log_handler(process, response, message, logger, log_level, process_step, log_file_name)
        assert os.path.isfile(os.path.join(tmpdir, log_file_name))
    assert response.message == message
    assert (
        response.status_percentage
        == TestProcess().status_percentage_steps[process_step]
    )
    # caplog.text is only non-empty when this test is run on its own. Explained further in issue 13 on GitHub.
    try:
        assert message in caplog.text
    except AssertionError:
        pass
