import re
from pywps.app.exceptions import ProcessError


def custom_process_error(err):
    """ProcessError from pywps only allows a limited list of valid chars
    in custom msgs or it reverts to it's default msg. By matching the end
    of a msg only and removing the '()' brackets and ' quote we can show
    some of the original error message to the user"""
    err_match = re.compile(r"[^:\n].*$").findall(str(err))
    err_msg = err_match[0].replace("(", "").replace(")", "").replace("'", "")
    raise ProcessError(f"{type(err).__name__}: {err_msg}")
