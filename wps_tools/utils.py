# Processor imports
from pywps import FORMATS, Process
from requests import head, get
from requests.exceptions import ConnectionError, MissingSchema, InvalidSchema
from pywps.inout.outputs import MetaLink4, MetaFile
from pywps.app.exceptions import ProcessError

# Tool import
from nchelpers import CFDataset

# Library imports
import logging
import os
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve
from collections import OrderedDict

MAX_OCCURS = 1000

common_status_percentages = {
    "start": 0,
    "process": 20,
    "build_output": 95,
    "complete": 100,
}


def url_handler(workdir, url):
    """Handles URL based on its type

    A process cannot access to the data from an HTTPServer URL without downloading
    while OPeNDAP URL can be treated as a filepath.
    The function returns the given URL if it is an OPeNDAP path.
    Otherwise, data from the HTTPServer URL are copied to a file created in workdir,
    and the path to the file is returned.

    Parameters:
        workdir (str): Path to the workdir
        url (str): URL to be handled

    Returns:
        url/local_file (str): URL/filepath with accessible data
    """
    if is_opendap_url(url):
        # OPeNDAP
        return url
    elif urlparse(url).scheme and urlparse(url).netloc:
        # HTTPServer or other
        local_file = os.path.join(workdir, url.split("/")[-1])
        urlretrieve(url, local_file)
        return local_file


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
            args[request.inputs[k][0].identifier] = request.inputs[k][0].data
        elif vars(request.inputs[k][0])["_url"] != None:
            # OPeNDAP or HTTPServer
            args[request.inputs[k][0].identifier] = url_handler(
                workdir, request.inputs[k][0].url
            )
        elif os.path.isfile(request.inputs[k][0].file):
            # Local files
            args[request.inputs[k][0].identifier] = request.inputs[k][0].file

    return args


def is_opendap_url(url):  # From Finch bird
    """Check if a provided url is an OpenDAP url

    The DAP Standard specifies that a specific tag must be included in the
    Content-Description header of every request. This tag is one of:
        "dods-dds" | "dods-das" | "dods-data" | "dods-error"
    So we can check if the header starts with `dods`.
    Even then, some OpenDAP servers seem to not include the specified header...
    So we need to let the netCDF4 library actually open the file.

    Parameters:
        url (str): Provided url

    Returns:
        bool: True if url is OpenDAP, False otherwise
    """
    try:
        content_description = head(url, timeout=5).headers.get("Content-Description")
    except (ConnectionError, MissingSchema, InvalidSchema):
        return False

    if content_description:
        return content_description.lower().startswith("dods")
    else:
        try:
            dataset = CFDataset(url)
        except OSError:
            return False
        return dataset.disk_format in ("DAP2", "DAP4")


def get_filepaths(nc_input):
    """Collect list of netcdf file paths

    Each path in nc_input is checked to determine if it is an OpenDAP url. If so,
    then the url is appended to the path list. If not, then whether or not it's a valid
    netcdf file is checked. If so, then the path is appended to the list. If not, then 
    a ProcessError is raised due to an invalid input.

    Parameters:
        nc_input (pywps.ComplexInput): Object containing local or OpenDAP file paths

    Returns:
        list: List of filepaths
    """
    filepaths = []
    for path in nc_input:
        if is_opendap_url(path.url):
            filepaths.append(path.url)
        elif path.file.endswith(".nc"):
            filepaths.append(path.file)
        else:
            raise ProcessError(
                "You must provide a data source (opendap/netcdf). "
                f"Inputs provided: {nc_input}"
            )
    return filepaths


def collect_output_files(varname, outdir=os.getcwd()):
    """Collect output netcdf files

    The given directory is searched for the files that contain
    the given variable name, indicating that these files were outputted
    by the same process. Though the default directory is the current directory,
    it is most often the current WPS process's working directory.
    
    Parameters:
        varname (str): Name of variable (must be in file names)
        outdir (str): Directory containing output files

    Returns:
        list: List of output files
    """
    return [file for file in os.listdir(outdir) if varname in file]


def build_meta_link(
    varname,
    desc,
    outfiles,
    format_name="netCDF",
    fmt=FORMATS.NETCDF,
    outdir=os.getcwd(),
):
    """Create meta link between output files

    A MetaLink4 object is created to contain a description of the
    process output, and a MetaFile is created for each output file to be
    appended to this link.

    Parameters:
        varname (str): Name of variable (used for MetaLink4)
        desc (str): Description of meta file
        outfiles (list): List of output files
        format_name (str): Format name of output files
        fmt (pywps.FORMATS): Format of output files
        outdir (str): Directory containing output files

    Returns:
        MetaLink4.xml: xml of metalink connecting output files
    """
    if len(outfiles) == 1:
        meta_link = MetaLink4(
            "output", f"Output of {format_name} {varname} file", workdir=outdir
        )
    else:
        meta_link = MetaLink4(
            "output", f"Output of {format_name} {varname} files", workdir=outdir
        )

    for file in outfiles:
        # Create a MetaFile instance, which instantiates a ComplexOutput object.
        meta_file = MetaFile(f"{file}", desc, fmt=fmt)
        meta_file.file = os.path.join(outdir, file)
        meta_link.append(meta_file)

    return meta_link.xml


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


def copy_http_content(http, file):
    """
        This function is implemented to copy the content of a file passed
        as an http address to a local file.

        Parameters:
            http (str): http address containing the desired content
            file (file object): path to the 
                file that the content will be copied to
        Returns:
            Path to the copied file in /tmp directory
        """
    file.write(get(http).content)
    return file.name
