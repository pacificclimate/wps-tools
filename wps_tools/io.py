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


def collect_args(request, workdir):
    """Collects PyWPS input arguments

    There are 3 ways to retrieve PyWPS input arguments depending on their types:
        .data is used to retrieve the data provided as LiteralInput
        .url is used to retrieve the URL path to the input provided as ComplexInput
        .file is used to retrieve the filepath to the input provided as ComplexInput

    The function collects and returns the retrieved arguments in an OrderedDict for
    versatility. Items are ordered in the sequence of "inputs" list of a process

    Parameters:
        request (pywps.app.WPSRequest.WPSRequest): PyWPS request that carries inputs
        workdir (str): Path to the workdir

    Returns:
        args (OrderedDict): keys are identifiers and values are input arguments
    """
    args = OrderedDict()
    for k in request.inputs.keys():
        if "data_type" in vars(request.inputs[k][0]).keys():
            # LiteralData
            args[request.inputs[k][0].identifier] = [
                request.inputs[k][i].data for i in range(0, len(request.inputs[k]))
            ]
        elif vars(request.inputs[k][0])["_url"] != None:
            # OPeNDAP or HTTPServer
            args[request.inputs[k][0].identifier] = [
                url_handler(workdir, request.inputs[k][i].url)
                for i in range(0, len(request.inputs[k]))
            ]
        elif os.path.isfile(request.inputs[k][0].file):
            # Local files
            args[request.inputs[k][0].identifier] = [
                request.inputs[k][0].file for i in range(0, len(request.inputs[k]))
            ]

    return args
