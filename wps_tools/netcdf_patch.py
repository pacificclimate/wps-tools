"""
Monkey-patch netCDF4.getlibversion to strip development suffixes like '-development',
which are incompatible with distutils.StrictVersion used in the birdy library.
"""

import netCDF4


def apply_netcdf4_version_patch():
    """Apply monkey patch to fix netCDF4 development version string parsing."""
    if hasattr(netCDF4, "_original_getlibversion"):
        return

    # Store original function
    netCDF4._original_getlibversion = netCDF4.getlibversion

    def patched_getlibversion():
        version = netCDF4._original_getlibversion()
        clean_version = version.split("-")[0].split(" ")[0]
        # Maintain original format but with clean version
        return f"{clean_version} NC_64BIT_DATA"

    netCDF4.getlibversion = patched_getlibversion


# Auto-apply when imported
apply_netcdf4_version_patch()
