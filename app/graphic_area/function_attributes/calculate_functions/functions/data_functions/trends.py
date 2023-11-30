import numpy as np
import pandas as pd



def trend(type: str, a: float, b: float, step: float, N: int) -> list:    
    trend_type_to_function = {
    "linear_rising": lambda t, a, b: a * t + b,
        "linear_falling": lambda t, a, b: -a * t + b,
        "nonlinear_rising": lambda t, a, b: b * np.exp(a * t),
        "nonlinear_falling": lambda t, a, b: b * np.exp(-a * t),
    }

    t = np.arange(0, N * step, step)

    data = None
    if type in trend_type_to_function:
        data = trend_type_to_function[type](t, a, b)

    df = pd.DataFrame({'x': t, 'y': data})
    return df