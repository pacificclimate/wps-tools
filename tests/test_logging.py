import pytest
import logging
import os
from collections import namedtuple
import tempfile
from pkg_resources import resource_filename
from wps_tools.utils import log_handler
from .common import Response
from .processes.wps_test_process import TestProcess

logging.root.setLevel(logging.INFO)
logger = logging.getLogger()

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: wps-tools: %(message)s", "%Y-%m-%d %H:%M:%S"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


@pytest.mark.parametrize(("message"), ["Process completed"])
@pytest.mark.parametrize(("process_step"), ["complete"])
@pytest.mark.parametrize(("level"), ["INFO"])
def test_log_handler(message, process_step, level, caplog):
    process = TestProcess()
    response = Response()
    with tempfile.TemporaryDirectory() as tmpdir:  # For storing temporary log.txt file
        process.workdir = tmpdir
        logger.setLevel(level)
        logger.log(logger.level, message)
        log_handler(
            process, response, message=message, logger=logger, process_step=process_step
        )
        assert os.path.isfile(os.path.join(tmpdir, "log.txt"))
    assert response.message == message
    assert (
        response.status_percentage
        == TestProcess().status_percentage_steps[process_step]
    )
    try:
        assert message in caplog.text
    except AssertionError:
        pass
