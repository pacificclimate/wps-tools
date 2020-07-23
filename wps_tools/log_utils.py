# Library imports
import logging
import os

pywps_logger = logging.getLogger("PYWPS")
stderr_logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: thunderbird: %(message)s", "%Y-%m-%d %H:%M:%S"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
stderr_logger.addHandler(handler)
stderr_logger.setLevel(stderr_logger.level)


def log_handler(process, response, message, process_step=None, level="INFO"):
    if process_step:
        status_percentage = process.status_percentage_steps[process_step]
    else:
        status_percentage = response.status_percentage

    # Log to all sources
    pywps_logger.log(getattr(logging, level), message)
    stderr_logger.log(getattr(logging, level), message)
    response.update_status(message, status_percentage=status_percentage)
