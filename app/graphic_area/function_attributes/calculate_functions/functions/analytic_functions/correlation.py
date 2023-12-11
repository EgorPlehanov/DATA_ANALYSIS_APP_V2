from ....function_typing import FunctionResult

import numpy as np
from pandas import DataFrame
from typing import Literal


def acf(
    data: DataFrame,        # Набор данных (из другой функции)
    function_type: Literal[ # Тип функции: 'autocorrelation' | 'covariance'
        'autocorrelation', 'covariance'
    ]  
) -> FunctionResult:
    '''
    Автокорреляция/Ковариация
    '''
    if data is None:
        return FunctionResult()
    
    y = data.iloc[:, 1].copy()
    N = len(y)

    y_mean = np.mean(y)
    L_values = np.arange(0, N)
    ac_values = []

    for L in L_values:
        if function_type == 'autocorrelation':
            ac = sum([(y[k] - y_mean) * (y[k + L] - y_mean) for k in range(0, N-L-1)]) / sum((y - y_mean)**2)
        elif function_type == 'covariance':
            ac = np.sum([(y[k] - y_mean) * (y[k+L] - y_mean) for k in range(0, N-L-1)]) / N

        ac_values.append(ac)
    
    result_df = DataFrame({'L': L_values, 'AC': ac_values})
    return FunctionResult(main_data=result_df)


def ccf(
    first_data: DataFrame,  # Первый набор данных (из другой функции)
    second_data: DataFrame, # Второй набор данных (из другой функции)
) -> FunctionResult:
    '''
    Кросс-корреляция
    '''
    if first_data is None or second_data is None:
        return FunctionResult()
    
    first_values = first_data.iloc[:, 1].copy()
    first_N = len(first_values)

    second_values = second_data.iloc[:, 1].copy()
    second_N = len(second_values)

    N = first_N if first_N < second_N else second_N

    L_values = np.arange(0, N)
    first_mean = np.mean(first_values)
    second_mean = np.mean(second_values)
    
    ccf_values = []
    for L in L_values:
        ccf_L = sum([
            (first_values[k] - first_mean) * (second_values[k + L] - second_mean)
            for k in range(0, N-L-1)
        ]) / N
        ccf_values.append(ccf_L)
    
    result_df = DataFrame({'L': L_values, 'AC': ccf_values})
    return FunctionResult(main_data=result_df)
