import io
import sys
from typing import Callable, Any


def capture_print(function: Callable, *args: Any) -> str:
    captured_output = io.StringIO()  # Create StringIO object
    before_redirect_stdout = sys.stdout
    sys.stdout = captured_output  # and redirect stdout.
    function(*args)  # this funtions prints get captured
    sys.stdout = before_redirect_stdout  # Reset redirect.
    captured_output_str = captured_output.getvalue()
    print(captured_output_str)  # print to make sure that the output shows
    return captured_output_str
