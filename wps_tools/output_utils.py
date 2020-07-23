# Processor imports
from pywps import FORMATS
from pywps.inout.outputs import MetaLink4, MetaFile

# Library import
import os

MAX_OCCURS = 1000


def collect_output_files(varname, outdir=os.getcwd()):
    """
    Collect output netcdf files.

    Parameters:
        varname (str): name of variable (must be in filenames)
        outdir (str): Directory containing output files
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
    """
    Create meta link between output netcdf files.

    Parameters:
        varname (str): name of variable (used for MetaLink4)
        desc (str): Description of meta file
        outfiles (list): List of output files
        format_name (str): Format name of output files
        fmt (FORMATS): Format of output files
        outdir (str): Directory containing output files
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
