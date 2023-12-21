from ....function_typing import FunctionResult, ResultData


import numpy as np
import pandas as pd


def test(
    cb,
    ddfd,
    dd,
    fp,
    sl,
    sw,
    tfdt,
    tf,
    dl
) -> FunctionResult:
    error_message = f"Заданые значения:\n" \
        + f"cb = {cb},\n" \
        + f"ddfd = {ddfd},\n" \
        + f"dd = {dd},\n" \
        + f"fp = {fp},\n" \
        + f"sl = {sl},\n" \
        + f"sw = {sw},\n" \
        + f"tfdt = {tfdt},\n" \
        + f"tf = {tf},\n" \
        + f"dl = {dl}"

    data = pd.DataFrame({'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'y': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    return FunctionResult(
        main_data = data,
        extra_data = None,
        error_message = error_message
    )