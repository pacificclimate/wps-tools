from rpy2 import robjects
from rpy2.robjects.packages import isinstalled, importr
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
    robjects.r(f"load(file='{r_file}')")
    return robjects.r(r_object_name)


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