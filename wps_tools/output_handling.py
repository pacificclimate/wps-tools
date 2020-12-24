import json, requests, math

from netCDF4 import Dataset
from tempfile import NamedTemporaryFile
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
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
        suffix=".json", prefix="tmp_copy", dir="/tmp", delete=True
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


def txt_to_string(url):
    with urlopen(url) as text:
        return text.read().decode("utf-8")


def get_available_robjects(url):
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True, mode="wb"
    ) as r_file:
        urlretrieve(url, r_file.name)
        objects = list(robjects.r(f"load(file='{r_file.name}')"))

    return objects


def auto_construct_outputs(get_output):
    process_outputs = []
    for value in get_output:
        if value.endswith(".rda") or value.endswith(".rdata"):
            output = load_rdata_to_python(value)

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

        process_outputs.append((output, type(output)))

    return process_outputs
