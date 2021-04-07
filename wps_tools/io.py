from pywps import LiteralInput, ComplexOutput, FORMATS, Format
from collections import OrderedDict
import os
import logging

from wps_tools.file_handling import url_handler

log_level = LiteralInput(
    "loglevel",
    "Log Level",
    default="INFO",
    abstract="Logging level",
    allowed_values=list(logging._levelToName.values()),
)


dryrun_input = LiteralInput(
    "dry_run",
    "Dry Run",
    abstract="Checks file to ensure compatible with process",
    data_type="boolean",
)


meta4_output = ComplexOutput(
    "output",
    "Output",
    as_reference=True,
    abstract="Metalink object between output files",
    supported_formats=[FORMATS.META4],
)

nc_output = ComplexOutput(
    "output",
    "Output",
    as_reference=True,
    abstract="Output Netcdf File",
    supported_formats=[FORMATS.NETCDF],
)

dryrun_output = ComplexOutput(
    "dry_output",
    "Dry Output",
    as_reference=True,
    abstract="File information",
    supported_formats=[FORMATS.TEXT],
)

meta4_dryrun_output = ComplexOutput(
    "dry_output",
    "Dry Output",
    as_reference=True,
    abstract="Metalink object between dry output files",
    supported_formats=[FORMATS.META4],
)

rda_output = ComplexOutput(
    "rda_output",
    "Rda output file",
    abstract="Rda file containing R output data",
    supported_formats=[
        Format("application/x-gzip", extension=".rda", encoding="base64")
    ],
)

vector_name = LiteralInput(
    "vector_name",
    "Output vector variable name",
    abstract="Name to label the output vector",
    default="output_vector",
    min_occurs=0,
    max_occurs=1,
    data_type="string",
)


def collect_args(inputs, workdir):
    """Collects PyWPS input arguments

    There are 4 ways to retrieve PyWPS input arguments depending on their types:
        LiteralInput
        - `.data` is used to retrieve the data

        ComplexInput
        - `.url` is used to retrieve the URL path
        - `.file` is used to retrieve the filepath
        - `.stream` is used to retrieve the datastream

    The function collects and returns the retrieved arguments in an OrderedDict for
    versatility. Items are ordered in the sequence of "inputs" list of a process

    Parameters:
        inputs (list): Collection of inputs provided by PyWPS
        workdir (str): Path to the workdir

    Returns:
        Dict containing processed inputs
    """

    def process_literal(input):
        return input.data

    def process_complex(input):
        if input["_url"] != None:
            return url_handler(workdir, input.url)

        elif input["_stream"] != None:
            return input.stream

        elif os.path.isfile(input.file):
            return input.file

        else:
            raise Exception("temp exception, need processerror")

    def process_input(multi_input):
        info = multi_input.json

        if info["type"] == "literal":
            return [process_literal(input) for input in multi_input]

        elif info["type"] == "complex":
            return [process_complex(input) for input in multi_input]

    return {input.identifier: process_input(input) for input in inputs}
