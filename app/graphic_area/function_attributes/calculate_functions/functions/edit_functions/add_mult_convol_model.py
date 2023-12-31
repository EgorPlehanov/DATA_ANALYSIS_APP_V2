from ....function_typing import FunctionResult, ResultData, Range

import numpy as np
from pandas import DataFrame


def add_model(
    first_data: DataFrame,  # Первый набор данных (из другой функции)
    second_data: DataFrame  # Второй набор данных (из другой функции)
) -> FunctionResult:
    '''
    Поэлементно складывает два набора данных
    '''
    if first_data is None or second_data is None:
        return FunctionResult()
    
    first_values = first_data.iloc[:, 1].copy()
    first_N = len(first_values)

    second_values = second_data.iloc[:, 1].copy()
    second_N = len(second_values)

    N = first_N if first_N < second_N else second_N

    result_df = DataFrame({
        'x': np.arange(0, N),
        'y': first_values.iloc[:N] + second_values.iloc[:N]
    })
    return FunctionResult(main_data=result_df)


def mult_model(
    first_data: DataFrame,   # Первый набор данных (из другой функции)
    second_data: DataFrame   # Второй набор данных (из другой функции)
) -> list:
    '''
    Поэлементно перемножает два набора данных
    '''
    if first_data is None or second_data is None:
        return FunctionResult()
    
    first_values = first_data.iloc[:, 1].copy()
    first_N = len(first_values)

    second_values = second_data.iloc[:, 1].copy()
    second_N = len(second_values)

    N = first_N if first_N < second_N else second_N

    result_df = DataFrame({
        'x': np.arange(0, N),
        'y': first_values.iloc[:N] * second_values.iloc[:N]
    })
    return FunctionResult(main_data=result_df)


def convol_model(
    first_data: DataFrame,   # Первый набор данных (из другой функции)
    second_data: DataFrame,  # Второй набор данных (из другой функции)
    M: int                   # Ширина окна
) -> FunctionResult:
    '''
    Дискретная светрка
    '''
    if first_data is None or second_data is None:
        return FunctionResult()
    
    first_values = first_data.iloc[:, 1].copy()
    first_N = len(first_values)

    second_values = second_data.iloc[:, 1].copy()
    second_N = len(second_values)

    N = first_N if first_N < second_N else second_N
    first_values = first_values[:N]
    second_values = second_values[:N]

    if M > N:
        raise ValueError('Ширина окна не может быть больше длины набора данных')

    y = np.zeros(N + M)

    for k in range(N + M):
        y[k] = sum([
            first_values[k - m] * second_values[m]
            for m in range(M)
            if k - m >= 0 and k - m < N
        ])

    y = y[M//2:-M//2]
    
    result_df = DataFrame({'x': np.arange(0, len(y)), 'y': y})
    test = np.convolve(first_values, second_values)
    extra_data = ResultData(DataFrame({'x': np.arange(0, len(test)), 'y': test}))
    return FunctionResult(main_data=result_df, extra_data=extra_data)


def extend_model(
    first_data: DataFrame,   # Первый набор данных (из другой функции)
    second_data: DataFrame   # Второй набор данных (из другой функции)
) -> FunctionResult:
    '''
    Объединение двух наборов данных
    '''
    if first_data is None or second_data is None:
        return FunctionResult()
    
    first_x = first_data.iloc[:, 0].copy()
    first_y = first_data.iloc[:, 1].copy()

    second_x = second_data.iloc[:, 0].copy()
    second_y = second_data.iloc[:, 1].copy()

    second_x = second_x + np.max(first_x)

    result_x = np.concatenate((first_x[:-1], second_x))
    result_y = np.concatenate((first_y[:-1], second_y))

    result_df = DataFrame({'x': result_x, 'y': result_y})
    return FunctionResult(main_data=result_df)


def cut_model(
    data: DataFrame, # Набор данных (из другой функции)
    range: Range     # Диапазон
) -> FunctionResult:
    '''
    Обрезать по краям набор данных
    '''
    if data is None:
        return FunctionResult()
    
    x = data.iloc[:, 0].copy()
    y = data.iloc[:, 1].copy()
    N = len(x)

    start = int(range.start_value / 100 * N) 
    end = int(range.end_value / 100 * N)

    result_x = x[start:end]
    result_y = y[start:end]

    result_x = result_x - np.min(result_x)

    result_df = DataFrame({'x': result_x, 'y': result_y})
    return FunctionResult(main_data=result_df)