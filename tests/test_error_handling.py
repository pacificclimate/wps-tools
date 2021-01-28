import pytest
from pywps.app.exceptions import ProcessError
from wps_tools.error_handling import custom_process_error


@pytest.mark.parametrize(
    ("err", "expected_msg"),
    [
        (
            ValueError("ValueError:\n That's an invalid value (Error)"),
            "Thats an invalid value Error",
        ),
        (TypeError("type of error?:\n 'type' (error)"), "type error"),
    ],
)
def test_custom_process_error(err, expected_msg):
    with pytest.raises(ProcessError) as e:
        custom_process_error(err)

    assert str(e.value) == f"{type(err).__name__}:  {expected_msg}"
