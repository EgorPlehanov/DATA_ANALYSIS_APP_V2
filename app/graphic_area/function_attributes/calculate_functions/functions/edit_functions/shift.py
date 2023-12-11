from ....function_typing import FunctionResult

import numpy as np
import pandas as pd
from pandas import DataFrame


def shift(
    data: DataFrame,    # Набор данных (из другой функции)
    C: float,           # Значение сдвига
    N1: int,            # Начальный индекс интервала
    N2: int             # Конечный индекс интервала
) -> FunctionResult:
    """
    Сдвигает данные data в интервале [N1, N2] на константу C.
    """
    if data is None:
        return FunctionResult()
    
    N1, N2 = int(N1), int(N2)
    if N1 > N2:
        N1, N2 = N2, N1

    N = len(data)

    error_message = None
    if N1 < 0 or N2 > N:
        error_message = "Некорректное значение N1 или N2: " \
            + f"0 <= N1 <= N2 <= {N}, значения N1 = {N1}, N2 = {N2}"

    if N1 > N and N2 > N:
        error_message = f'Некорректные значения N1 и N2: " \
            "N1 и N2 должны быть <= {N}, значения N1 = {N1}, N2 = {N2}'
        raise ValueError(error_message)

    shifted_values = data.iloc[:, 1].copy()
    shifted_values[N1:N2+1] += C

    shifted_df = pd.DataFrame({'x': data.iloc[:, 0].copy(), 'y': shifted_values})
    return FunctionResult(main_data=shifted_df, error_message=error_message)


def anti_shift(
    data: DataFrame  # Набор данных (из другой функции)
) -> FunctionResult:
    '''
    Убирает смещение данных
    '''
    if data is None:
        return FunctionResult()
        
    y_values = data.iloc[:, 1].copy()
    mean_value = np.mean(y_values)
    y_values -= mean_value

    no_shift_df = pd.DataFrame({'x': data.iloc[:, 0].copy(), 'y': y_values})
    return FunctionResult(main_data=no_shift_df)
