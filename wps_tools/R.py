import re
from rpy2 import robjects
from rpy2.robjects.packages import isinstalled, importr
from rpy2.rinterface_lib.embedded import RRuntimeError
from pywps.app.exceptions import ProcessError


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
