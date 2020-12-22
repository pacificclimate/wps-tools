import logging
from pathlib import Path

common_status_percentages = {
    "start": 0,
    "process": 20,
    "build_output": 95,
    "complete": 100,
}


def log_handler(
    process,
    response,
    message,
    logger,
    log_level="INFO",
    process_step=None,
    log_file_name="log.txt",
):
    """Output message to logger and update response status

    A message is outputted to a logger and log file at the specified level, and
    the progress status of the response is updated according to the specified
    process step. The log file is stored in the process's working directory.

    Parameters:
        process (pywps.Process): Currently running WPS process
        response (pywps.WPSResponse): Response object for process
        message (str): Message to be outputted
        logger (logging.Logger): Logger to store messages
        log_level (str): Logging level at which to output message
        process_step (str): Current stage of process execution
        log_file_name (str): File to store logger content
    """
    if process_step:
        status_percentage = process.status_percentage_steps[process_step]
    else:
        status_percentage = response.status_percentage

    # Log to all sources
    logger.log(getattr(logging, log_level), message)
    log_file_path = Path(process.workdir) / log_file_name  # From Finch bird
    log_file_path.open("a", encoding="utf8").write(message + "\n")
    response.update_status(message, status_percentage=status_percentage)
