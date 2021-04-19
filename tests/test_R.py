import pytest
from pkg_resources import resource_filename
from tempfile import NamedTemporaryFile
from rpy2 import robjects
from wps_tools.R import (
    get_package,
    load_rdata_to_python,
    save_python_to_rdata,
    r_valid_name,
    get_robjects,
)
from wps_tools.testing import local_path
from pywps.app.exceptions import ProcessError


@pytest.mark.parametrize(
    ("package"), [("base"), ("utils")],
)
def test_get_package(package):
    pkg = get_package(package)
    assert pkg.__dict__["__rname__"] == package


@pytest.mark.parametrize("package", ["invalid_pkg"])
def test_get_package_err(package):
    with pytest.raises(ProcessError) as e:
        get_package(package)
        assert str(vars(e)["_excinfo"][1]) == f"R package, {package}, is not installed"


@pytest.mark.parametrize(
    ("r_file", "r_object_name"),
    [(resource_filename(__name__, "data/expected_gsl.rda"), "expected_gsl_vector")],
)
def test_load_rdata_to_python(r_file, r_object_name):
    r2py_object = load_rdata_to_python(r_file, r_object_name)
    assert "robjects" in str(type(r2py_object))

    robjects.r("rm(list=ls())")


@pytest.mark.parametrize(
    ("file_", "obj_name"),
    [(resource_filename("tests", "data/expected_days_data.rda"), "autumn_days"),],
)
def test_load_rdata_to_python_err(file_, obj_name):
    with pytest.raises(ProcessError) as e:
        load_rdata_to_python(file_, obj_name)
    assert (
        str(vars(e)["_excinfo"][1])
        == "RRuntimeError: The variable name passed is not an object found in the given rda file"
    )


@pytest.mark.parametrize(
    ("r_name", "py_var"), [("str_ex", "string"), ("int_ex", 300),],
)
def test_save_python_to_rdata(r_name, py_var):
    with NamedTemporaryFile(
        suffix=".rda", prefix="tmp_copy", dir="/tmp", delete=True
    ) as r_file:
        save_python_to_rdata(r_name, py_var, r_file.name)
        test_var = load_rdata_to_python(r_file.name, r_name)

    assert test_var[0] == py_var

    robjects.r("rm(list=ls())")


@pytest.mark.parametrize(
    ("name"), [("hello.world"), ("r_name")],
)
def test_r_valid_name(name):
    r_valid_name(name)


@pytest.mark.parametrize(
    ("name"), [(".2"), ("if"), ("two words")],
)
def test_r_valid_name_err(name):
    with pytest.raises(ProcessError) as e:
        r_valid_name(name)
    assert str(vars(e)["_excinfo"][1]) == "Your vector name is not a valid R name"


@pytest.mark.parametrize(
    ("url"), [(local_path("expected_gsl.rda")), (local_path("expected_days_data.rda"))]
)
def test_get_robjects(url):
    objects = get_robjects(url)

    assert len(objects) > 0
    for ob in objects:
        assert isinstance(ob, str)
