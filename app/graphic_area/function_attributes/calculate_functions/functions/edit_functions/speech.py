from ....function_typing import FunctionResult, Range

from typing import Dict
import numpy as np
import pandas as pd
from pandas import DataFrame


def rw(
    data: DataFrame,        # Набор данных (из другой функции)
    start_end_coef: Dict,   # Словарь диапазонов с коэффициентами
) -> FunctionResult:
    """
    Домножает данные в диапазоне на коэффициент
    """
    if data is None:
        return FunctionResult()
    
    error_message = None
    
    y_values = data.iloc[:, 1].copy()
    N = len(y_values)

    for row_idx, params in start_end_coef.items():
        start = (params['start'])
        end = (params['end'])
        coef = float(params['coef'])

        if start > end:
            start, end = end, start

        if not(0 <= start <= N and 0 <= end <= N):
            message = f'Некорректные значения start и end в строке {row_idx}: они ' \
                + f'должны быть от 0 до {N}, значения "start" = {start}, "end" = {end}"'
            if error_message is None:
                error_message = message
            else:
                error_message += '\n' + message
            continue

        y_values[start:end+1] *= coef

    edited_df = pd.DataFrame({'x': data.iloc[:, 0].copy(), 'y': y_values})
    return FunctionResult(main_data=edited_df, error_message=error_message)