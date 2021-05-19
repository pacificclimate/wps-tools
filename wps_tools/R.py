import re
from rpy2 import robjects
from rpy2.robjects.packages import isinstalled, importr
from rpy2.rinterface_lib.embedded import RRuntimeError
from pywps.app.exceptions import ProcessError
from tempfile import NamedTemporaryFile
from urllib.request import urlretrieve
from pkg_resources import resource_filename


def get_package(package):
    """
        Exposes all R objects in package as Python objects after
        checking that it is installed.

        Parameters:
            package (str): the name of an R package

        Returns:
            Exposed R package
    """
    if isinstalled(package):
        return importr(package)
    else:
        raise ProcessError(f"R package, {package}, is not installed")


def load_rdata_to_python(r_file, r_object_name):
    """
        Loads R objects from a .rda or .Rdata file into the embedded R
        environment, then exposes that object as a Python object.

        Parameters:
            r_file (str): path to an .rda or .rdata file
            r_object_name (str): name of an R object from the r_file

        Returns:
            Exposed R object as a python object
    """
    try:
        robjects.r(f"load(file='{r_file}')")
        obj = robjects.r(r_object_name)
        return obj
    except RRuntimeError as e:
        err_name = re.compile(r"object \'(.*)\' not found").findall(str(e))
        if "_" in err_name[0]:
            raise ProcessError(
                msg=f"{type(e).__name__}: The variable name passed is not an object found in the given rda file"
            )
        else:
            raise ProcessError(
                msg=f"{type(e).__name__}: There is no object named {err_name[0]} in this rda file"
            )


def save_python_to_rdata(r_name, py_var, r_file):
    """
        Saves a Python object as an R object to a Rdata (.rda) file

        Parameters:
            r_name (str): name to give the oject in the R environment
            py_var (any type): python variable to save to the R environment
            r_file (str): path to rdata file
    """
    robjects.r.assign(r_name, py_var)
    robjects.r(f"save({r_name}, file='{r_file}')")


def r_valid_name(robj_name):
    """The R function 'make.names' will change a name if it
    is not syntactically correct and leave it if it is

    Parameters:
        robj_name (str): The name of the robject to verify
    """
    base = get_package("base")
    if base.make_names(robj_name)[0] != robj_name:
        raise ProcessError(msg="Your vector name is not a valid R name")


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


def construct_r_out(outputs):
    """Build list of R outputs"""
    r_out = []
    for value in outputs:
        if value.endswith(".rda") or value.endswith(".rdata"):
            r_out.append([rda_to_vector(value, obj) for obj in get_robjects(value)])
    return r_out


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


def test_rda_output(url, vector_name, expected_file, expected_vector_name):
    """Testing method to check rda results"""
    output_vector = rda_to_vector(url, vector_name)
    local_path = resource_filename("tests", f"data/{expected_file}")
    expected_url = f"file://{local_path}"
    expected_vector = rda_to_vector(expected_url, expected_vector_name)

    for index in range(len(expected_vector)):
        assert str(output_vector[index]) == str(expected_vector[index])

    # Clear R global env
    robjects.r("rm(list=ls())")
