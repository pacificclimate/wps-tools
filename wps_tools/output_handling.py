import json, requests, math

from netCDF4 import Dataset
from tempfile import NamedTemporaryFile
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from rpy2 import robjects

from wps_tools.file_handling import copy_http_content
from wps_tools.R import load_rdata_to_python, get_package


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


def rda_to_vector(url, vector_name):
    """
    Access content from a rda url file as a Rpy2 vector object

    Parameters:
        url (str): file or http url path to a rda file
        vector_name (str): the name the vector was given when it
            was saved to the rda file

    Returns:
        Rpy2 object: Rpy2 representation of the R object "vector_name"
    """
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True, mode="wb"
    ) as r_file:
        urlretrieve(url, r_file.name)
        vector = load_rdata_to_python(r_file.name, vector_name)

    return vector


def vector_to_dict(url, vector_name):
    """
    Access content from a rda url file as a Python dictionary

    Parameters:
        url (str): file or http url path to a rda file containing
            a named vector object
        vector_name (str): the name the vector was given when it
            was saved to the rda file

    Returns:
        dictionary: Python dictionary representation of a named
            R vector
    """
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True, mode="wb"
    ) as r_file:
        urlretrieve(url, r_file.name)
        vector = load_rdata_to_python(r_file.name, vector_name)

    try:
        base = get_package("base")

        return {
            (base.names(vector)[index]): (
                None if math.isnan(vector[index]) else vector[index]
            )
            for index in range(len(vector))
        }
    except TypeError as e:
        print(f"{e}: {vector_name} is not a named vector")
        raise


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


def get_robjects(url):
    """
    Get a list of all the objects stored in an rda file

    Parameters:
        url (str): file or http url path to a rda file

    Returns:
        list: a list of the names of objects stored in an rda file
    """
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True, mode="wb"
    ) as r_file:
        urlretrieve(url, r_file.name)
        robjs = list(robjects.r(f"load(file='{r_file.name}')"))

    return robjs


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
        if value.endswith(".rda") or value.endswith(".rdata"):
            output = [rda_to_vector(value, obj) for obj in get_robjects(value)]

        elif value.endswith(".nc"):
            output = nc_to_dataset(value)

        elif value.endswith(".json"):
            output = json_to_dict(value)

        elif value.endswith(".txt"):
            output = txt_to_string(value)

        elif value.endswith(".meta4"):
            req = requests.get(value)
            metalinks = BeautifulSoup(
                BeautifulSoup(req.content.decode("utf-8")).prettify()
            ).find_all("metaurl")
            auto_construct_outputs([metalink.get_text() for metalink in metalinks])

        else:
            output = value

        process_outputs.extend(output if type(output) == list else [output])

    return process_outputs