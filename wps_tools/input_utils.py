# Processor imports
from requests import head
from requests.exceptions import ConnectionError, MissingSchema, InvalidSchema
from pywps.app.exceptions import ProcessError

# Tool import
from nchelpers import CFDataset

MAX_OCCURS = 1000  # Maximum permissible occurences of a given pywps input


def is_opendap_url(url):  # From Finch bird
    """
    Check if a provided url is an OpenDAP url.
    The DAP Standard specifies that a specific tag must be included in the
    Content-Description header of every request. This tag is one of:
        "dods-dds" | "dods-das" | "dods-data" | "dods-error"
    So we can check if the header starts with `dods`.
    Even then, some OpenDAP servers seem to not include the specified header...
    So we need to let the netCDF4 library actually open the file.
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


def get_filepaths(request):
    filepaths = []
    for path in request.inputs["netcdf"]:
        if is_opendap_url(path.url):
            filepaths.append(path.url)
        elif path.file.endswith(".nc"):
            filepaths.append(path.file)
        else:
            raise ProcessError(
                "You must provide a data source (opendap/netcdf). "
                f"Inputs provided: {request.inputs}"
            )
    return filepaths
