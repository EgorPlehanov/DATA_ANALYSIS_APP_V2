from ....function_typing import FunctionResult, ResultData

import numpy as np
import pandas as pd
from pandas import DataFrame


def generate_spikes(
    N: int,     # Длина данных
    M: int,     # Количество выбросов
    R: float,   # Опорное значение
    Rs: float   # Диапазон варьирования амплитуды
) -> DataFrame:
    '''
    Генерирует M случайных выбросов (спайков) на интервале [0, N] со случайными амплитудами
    '''
    spike_indices = np.random.choice(N, M, replace=False)
    spike_amplitudes = R + np.random.uniform(-Rs, Rs, M)
    spike_signs = np.random.choice([-1, 1], M)  # Выбираем случайный знак для выбросов

    data_values = np.zeros(N)
    data_values[spike_indices] = spike_signs * spike_amplitudes

    return DataFrame({'x': np.arange(N), 'y': data_values})


def spikes(
    data: DataFrame,    # Набор данных (из другой функции)
    N: int,             # Длина данных
    M: int,             # Количество выбросов
    R: float,           # Опорное значение
    Rs: float           # Диапазон варьирования амплитуды
) -> FunctionResult:
    """
    Генерирует M случайных выбросов (спайков) на интервале [0, N] со случайными амплитудами.
    """
    N, M = int(N), int(M)

    if data is None:
        if N < M:
            raise ValueError(
                "Некорректное количество выбросов, "
                + f"должно быть: M <= N. M = {M}, N = {N}"
            )

        error_message = None
        if M < 0.005 * N or M > 0.01 * N:
            error_message = "Некорректное количество выбросов: " \
                + f"M должно быть в пределах [{round(0.005*N)}, {round(0.01*N)}]"
            
        spikes_data = generate_spikes(N, M, R, Rs)
        return FunctionResult(main_data=spikes_data, error_message=error_message)
    
    N = len(data)
    if N < M:
        raise ValueError(
            "Некорректное количество выбросов, "
            + f"должно быть: M <= N. M = {M}, N = {N}"
        )

    error_message = None
    if M < 0.005 * N or M > 0.01 * N:
        error_message = "Некорректное количество выбросов: " \
            + f"M должно быть в пределах [{round(0.005*N)}, {round(0.01*N)}]"
    
    spikes_df = generate_spikes(N, M, R, Rs)
    extra_data = [ResultData(type='spikes', main_data=spikes_df)]

    data_spikes_df = pd.DataFrame({'x': data.get('x').copy(), 'y': data['y'] + spikes_df['y']})
    return FunctionResult(main_data=data_spikes_df, extra_data=extra_data, error_message=error_message)



def anti_spikes(
    data: DataFrame,    # Набор данных (из другой функции)
    R: float       # Порог (сравнение предыдущего и следующего значения с текущим)
) -> FunctionResult:
    '''
    Подавляет непровдопадобные значения методом 3-х точечной линейной интерполяции
    '''
    if data is None:
        return FunctionResult()
    
    y_values = data.get('y').copy()
    N = len(y_values)

    proc_data = np.copy(y_values)
    for i in range(1, N-1):
        if abs(y_values[i] - y_values[i-1]) > R and abs(y_values[i] - y_values[i+1]) > R:
            proc_data[i] = (y_values[i-1] + y_values[i+1]) / 2

    no_spikes_df = pd.DataFrame({'x': data.get('x').copy(), 'y': proc_data})
    return FunctionResult(main_data=no_spikes_df)
