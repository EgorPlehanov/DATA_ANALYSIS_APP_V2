from ....function_typing import FunctionResult

import sympy as sp
import numpy as np
import pandas as pd


def custom_function(
    expression: str,    # Расчетная функция
    N: int,             # Длина данных
    step: int           # Шаг генерации данных
) -> FunctionResult:
    '''
    Создает набор данных по расчетной функции
    '''
    if not expression:
        raise ValueError("Не задана расчетная функция")
    
    x = sp.symbols('x')

    math_expression = sp.sympify(expression)
    function = sp.lambdify(x, math_expression, "numpy")

    x_values = np.arange(0, N * step, step)
    y_values = [function(x) for x in x_values]

    data = pd.DataFrame({'x': x_values, 'y': y_values})
    return FunctionResult(main_data=data)
