import json, requests, math

from netCDF4 import Dataset
from tempfile import NamedTemporaryFile
from urllib.request import urlretrieve
from rpy2 import robjects

from wps_tools.file_handling import copy_http_content
from wps_tools.R import load_rdata_to_python, get_package


def nc_to_dataset(url):
    with NamedTemporaryFile(
        suffix=".nc", prefix="tmp_copy", dir="/tmp", delete=True
    ) as tmp_file:

        return Dataset(copy_http_content(url, tmp_file))


def json_to_dict(url):
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True
    ) as json_file:
        urlretrieve(url, json_file.name)

        return json.load(json_file)


def vector_to_dict(url, vector_name):
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True, mode="wb"
    ) as r_file:
        urlretrieve(url, r_file.name)
        vector = load_rdata_to_python(r_file.name, vector_name)

    base = get_package("base")

    return {
        (base.names(vector)[index]): (
            None if math.isnan(vector[index]) else vector[index]
        )
        for index in range(len(vector))
    }


def get_available_robjects(url):
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True, mode="wb"
    ) as r_file:
        urlretrieve(url, r_file.name)
        return robjects.r(f"load(file='{r_file.name}')")
