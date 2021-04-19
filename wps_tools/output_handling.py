import json, requests, math

from netCDF4 import Dataset
from tempfile import NamedTemporaryFile
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve

from wps_tools.file_handling import copy_http_content


def nc_to_dataset(url):
    """
    Access content of a netcdf file from an http url as a Dataset object
    using the netCDF4 library.

    Parameters:
        url (str): http url path to a netCDF file

    Returns:
        Dataset: Dataset object containing input netCDF file content
    """
    with NamedTemporaryFile(
        suffix=".nc", prefix="tmp_copy", dir="/tmp", delete=True
    ) as tmp_file:
        data = Dataset(copy_http_content(url, tmp_file))

    return data


def json_to_dict(url):
    """
    Access content from a json url file as a Python dictionary

    Parameters:
        url (str): file or http url path to a json file

    Returns:
        dictionary: Python dictionary with input json file's content
    """
    with NamedTemporaryFile(
        suffix=".json", prefix="tmp_copy", dir="/tmp", delete=True
    ) as json_file:
        urlretrieve(url, json_file.name)
        dictionary = json.load(json_file)

    return dictionary


def txt_to_string(url):
    """
    Access content from a txt url file as a string

    Parameters:
        url (str): file or http url path to a txt file

    Returns:
        string: content of the input txt file
    """
    with urlopen(url) as text:
        string = text.read().decode("utf-8")

    return string


def get_metalink_content(url):
    """
    Get a list of all the files from a metalink

    Parameters:
        url (str): file or http url path to a meta4 file

    Returns:
        list: a list of files
    """

    req = requests.get(url)
    metalinks = BeautifulSoup(
        BeautifulSoup(req.content.decode("utf-8"), features="lxml").prettify(),
        features="lxml",
    ).find_all("metaurl")

    return [
        metalink.get_text().replace("\n", "").replace(" ", "") for metalink in metalinks
    ]


def auto_construct_outputs(outputs):
    """
    Automatically construct Python objects from input url files.
    Written to construct complex WPS process Outputs.
    Parameters:
        outputs (list): list of file or http url paths to files
    Returns:
        list: the constructed python objects in a list
    """
    process_outputs = []
    for value in outputs:

        if value.endswith(".nc"):
            output = nc_to_dataset(value)

        elif value.endswith(".json"):
            output = json_to_dict(value)

        elif value.endswith(".txt"):
            output = txt_to_string(value)

        elif value.endswith(".meta4"):
            return auto_construct_outputs(get_metalink_content(value))

        else:
            output = value

        process_outputs.append(output)

    return process_outputs
