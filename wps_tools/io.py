from pywps import LiteralInput, ComplexInput, ComplexOutput, FORMATS, Format
import os
import logging
from pywps.app.exceptions import ProcessError
from wps_tools.file_handling import url_handler


# Inputs
dryrun_input = LiteralInput(
    "dry_run",
    "Dry Run",
    abstract="Checks file to ensure compatible with process",
    data_type="boolean",
)

log_level = LiteralInput(
    "loglevel",
    "Log Level",
    default="INFO",
    abstract="Logging level",
    allowed_values=list(logging._levelToName.values()),
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

csv_input = ComplexInput(
    "csv",
    "CSV document",
    abstract="A CSV document",
    supported_formats=[Format("text/csv", extension=".csv"), FORMATS.TEXT],
)

# Outputs
dryrun_output = ComplexOutput(
    "dry_output",
    "Dry Output",
    as_reference=True,
    abstract="File information",
    supported_formats=[FORMATS.TEXT],
)

meta4_output = ComplexOutput(
    "output",
    "Output",
    as_reference=True,
    abstract="Metalink object between output files",
    supported_formats=[FORMATS.META4],
)

meta4_dryrun_output = ComplexOutput(
    "dry_output",
    "Dry Output",
    as_reference=True,
    abstract="Metalink object between dry output files",
    supported_formats=[FORMATS.META4],
)

nc_output = ComplexOutput(
    "output",
    "Output",
    as_reference=True,
    abstract="Output Netcdf File",
    supported_formats=[FORMATS.NETCDF],
)

rda_output = ComplexOutput(
    "rda_output",
    "Rda output file",
    abstract="Rda file containing R output data",
    supported_formats=[
        Format("application/x-gzip", extension=".rda", encoding="base64")
    ],
)


def process_inputs_alpha(request_inputs, expected_inputs, workdir):
    """Process bird inputs and return them in alphabetical order

    This is meant to make it easier to track larger lists of inputs. It will
    also add in any missing inputs that were not given in the process.
    """
    requested = request_inputs.keys()
    all = [expected.identifier for expected in expected_inputs]
    missing_inputs = list(set(all) - set(requested))

    collected = collect_args(request_inputs, workdir)
    for missing_input in missing_inputs:
        collected[missing_input] = None

    # NOTE: If you want to find out the order of the variables, just uncomment
    #       these lines.
    # var_order = [name for name, value in sorted(collected.items())]
    # print(var_order)

    return [value for name, value in sorted(collected.items())]


def collect_args(inputs, workdir):
    """Collects PyWPS input arguments

    There are 4 ways to retrieve PyWPS input arguments depending on their types:
        LiteralInput
        - `.data` is used to retrieve the data

        ComplexInput
        - `.url` is used to retrieve the URL path
        - `.file` is used to retrieve the filepath
        - `.stream` is used to retrieve the csv datastreams

    Parameters:
        inputs (dict): Collection of inputs provided by PyWPS
        workdir (str): Path to the workdir

    Returns:
        Dict containing processed inputs
    """

    def process_literal(input):
        """Handler for LiteralInputs"""
        return input.data

    def process_complex(input):
        """Handler for ComplexInputs"""
        if "csv" in vars(input)["identifier"]:
            return input.stream

        # Check for a remote URL: try the new 'url' attribute, falling back to the legacy '_url'
        url_val = getattr(input, "url", None) or getattr(input, "_url", None)
        if url_val is not None:
            return url_handler(workdir, url_val)

        elif os.path.isfile(input.file):
            return input.file

        else:
            raise ProcessError("This input is not supported")

    def process_input(multi_input):
        """Process a list of inputs

        Each set of inputs from the outer function may or may not have multiple
        entries. The `multi_input` is just a list of Complex or Literal inputs
        that we iterate over.
        """
        first, *_ = multi_input
        info = first.json
        processor = process_literal if info["type"] == "literal" else process_complex

        if info["min_occurs"] > 1 or info["max_occurs"] > 1:
            return [processor(input) for input in multi_input]

        else:
            (input,) = multi_input
            return processor(input)

    return {identifier: process_input(input) for identifier, input in inputs.items()}
