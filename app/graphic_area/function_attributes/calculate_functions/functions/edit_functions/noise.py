from ....function_typing import FunctionResult, ResultData

import numpy as np
import pandas as pd
from pandas import DataFrame
import time
import random


def generate_noise(
    N: int,                     # Длина данных
    R: float,                   # Максимальное значение шума
    delta: float = None,        # Шаг генерации данных
    x_values: np.ndarray = None # Набор значений X
) -> DataFrame:
    '''
    Генерация случайного шума в заданном диапазоне [-R, R]
    '''
    noise_data = np.random.uniform(-R, R, N)

    # Пересчет данных в заданный диапазон R
    min_val, max_val = np.min(noise_data), np.max(noise_data)
    normalized_noise = ((noise_data - min_val) / (max_val - min_val) - 0.5) * 2 * R

    if x_values is None:
        if delta is None:
            delta = 1
        x_values = np.arange(0, N * delta, delta)

    return DataFrame({'x': x_values, 'y': normalized_noise})


def noise(
    data: DataFrame,    # Набор данных (из другой функции)
    N: int,             # Длина данных
    R: float,           # Максимальное значение шума
    delta: float        # Шаг генерации данных
) -> FunctionResult:
    '''
    Добавляет шум к выбранному набору данных
    '''
    if data is None:
        N = int(N)
        noise = generate_noise(N, R, delta)
        return FunctionResult(main_data=noise)
    
    N = len(data)
    
    noised_df = generate_noise(N, R, delta, data['x'].values)
    extra_data = [ResultData(type='noise', main_data=noised_df)]

    data_noised_df = pd.concat([data, noised_df]).groupby('x', as_index=False).sum()
    return FunctionResult(main_data=data_noised_df, extra_data=extra_data)


def generate_my_noise(
    N: int,                     # Длина данных
    R: float,                   # Максимальное значение шума
    delta: float,               # Шаг генерации данных
    x_values: np.ndarray = None # Набор значений X
) -> DataFrame:
    '''
    Генерация случайного шума в заданном диапазоне [-R, R] (Моя реализация)
    '''
    current_time = int(time.time())
    random.seed(current_time)

    custom_noise_data = [random.uniform(-R, R) for _ in range(N)]

    if x_values is None:
        x_values = np.arange(0, N * delta, delta)
    return pd.DataFrame({'x': x_values, 'y': custom_noise_data})


def my_noise(
    data: DataFrame,    # Набор данных (из другой функции)
    N: int,             # Длина данных
    R: float,           # Максимальное значение шума
    delta: float        # Шаг генерации данных
) -> FunctionResult:
    '''
    Добавляет шум к выбранному набору данных (Моя реализация)
    '''
    if data is None:
        N = int(N)
        my_noised = generate_noise(N, R, delta)
        return FunctionResult(main_data=my_noised)
    
    N = len(data)
    
    my_noised = generate_noise(N, R, delta, data['x'].values)
    extra_data = [ResultData(type='my_noise', main_data=my_noised)]

    data_noised_df = pd.concat([data, my_noised]).groupby('x', as_index=False).sum()
    return FunctionResult(main_data=data_noised_df, extra_data=extra_data)


def anti_noise(
    data: DataFrame,    # Набор данных (из другой функции)
    M: dict,            # Количество реализацй случайного шума
    R: float            # Опорное значение
) -> FunctionResult:
    '''
    Убирает случайный шум
    '''
    if data is None:
        return FunctionResult()
    
    # ВАРИАНТ 1
    x_values = data.get('x').copy()
    y_values = data.get('y').copy()
    N = len(y_values)

    # extra_data = []
    # std_deviation = []

    # M_values = sorted([int(m['M']) for m in M.values()])
    # for M in M_values:
        
    #     denoised_y = np.zeros(N)
    #     for _ in range(M):
    #         noise = generate_noise(N, R)['y']
    #         denoised_y += noise + y_values.copy()
    #     denoised_y = denoised_y / (M)

    #     # Расчет стандартной ошибки
    #     std_deviation.append(np.std(denoised_y))

    #     # Добавление расчета для M случайных шумов
    #     M_denoised_df = pd.DataFrame({'x': x_values, 'y': denoised_y})
    #     extra_data.append(ResultData(
    #         type=f'anti_noise(M={M})',
    #         main_data=M_denoised_df
    #     ))

    # # Добавление статистических данных
    # std_deviation_df = pd.DataFrame({'M': M_values, 'std': std_deviation})
    # extra_data.append(ResultData(
    #     type='anti_noise_M_std',
    #     main_data=std_deviation_df
    # ))
    

    # ВАРИАНТ 2
    noised_df = generate_noise(N, R, x_values=data['x'].values)
    data_noised_df = pd.concat([data, noised_df]).groupby('x', as_index=False).sum()
    data_noised_y = data_noised_df.get('y').copy()

    std_deviation = []
    extra_data = []

    M_values = [int(m['M']) for m in M.values()]
    for M in M_values:
        accumulated_noise = np.zeros(N)
        for _ in range(M):
            accumulated_noise += generate_noise(N, R)['y']

        norm_noise = accumulated_noise / M
        denoised_data = norm_noise + y_values

        std_deviation.append(np.std(norm_noise))

        M_denoised_df = pd.DataFrame({'x': x_values, 'y': denoised_data})
        extra_data.append(ResultData(
            type=f'anti_noise(M={M})',
            main_data=M_denoised_df
        ))

    std_deviation_df = pd.DataFrame({'M': M_values, 'std': std_deviation})
    extra_data.append(ResultData(
        type='anti_noise_M_std',
        main_data=std_deviation_df
    ))

    return FunctionResult(main_data=data_noised_df, extra_data=extra_data)
