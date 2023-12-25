from ....function_typing import FunctionResult, ResultData, File

from .filter import (
    fourier_spectrum, FilterType, lp_filter, hp_filter,
    bp_filter, bs_filter, convolution
)
from ..data_functions.download import read_data
from typing import Dict
import numpy as np
import pandas as pd
from pandas import DataFrame
from functools import partial



def convol_model(x, h, N, M):
    out_data = []
    for k in range(N):
        y = 0
        for m in range(M):
            if 0 <= k - m < len(x) and 0 <= m < len(h):
                y += x[k - m] * h[m]
        out_data.append(y)
    return out_data



def get_filtered_data_f(
    type: FilterType,   # Тип фильтра
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    m: int,             # Ширина окна Поттера
    Fc_down: float = None,  # Нижняя граница
    Fc_up: float = None,  # Верхняя граница
) -> FunctionResult:
    '''
    Функция для получения отфильтрованного сигнала
    '''
    filter_by_type = {
        # Филтр Низких Частот (ФНЧ)
        FilterType.lpf: partial(lp_filter, dt, Fc_up, m),
        # Филтр Высоких Частот (ФВЧ)
        FilterType.hpf: partial(hp_filter, dt, Fc_down, m),
        # Полосовый Фильтр (ПФ)
        FilterType.bpf: partial(bp_filter, dt, Fc_down, Fc_up, m),
        # Режекторный Фильтр (РФ)
        FilterType.bsf: partial(bs_filter, dt, Fc_down, Fc_up, m),
    }

    filter_values = filter_by_type[type]()
    x_values = data.iloc[:, 0].copy().to_list()
    y_values = data.iloc[:, 1].copy().to_list()

    M = 2 * m + 1
    convolve_data = convolution(y_values, filter_values, len(y_values), M)
    filtered_data = DataFrame({'x': x_values, 'y': convolve_data})
    
    return filtered_data 




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
    x_values = data.iloc[:, 0].copy()
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

    edited_df = pd.DataFrame({'x': x_values, 'y': y_values})
    return FunctionResult(main_data=edited_df, error_message=error_message)



def speach_process(
    library_data: File, # Файл с данными
    ranges: Dict,       # Словарь диапазонов с коэффициентами
    f_values: Dict,     # Сооварь частот формант
    m: int,             # Ширина окна Поттера
) -> FunctionResult:
    """
    Обработка аудео сигналов
    """
    if library_data is None:
        return FunctionResult()
    
    data = read_data(library_data.path).main_data
    
    error_message = None
    extra_data = []
    extra_data = [ResultData(
        main_data = fourier_spectrum(data),
        type = f'Спектр исходного сигнала',
    )]
    
    y = data.iloc[:, 1].copy()
    x = data.iloc[:, 0].copy()
    N = len(y)

    for row_idx, params in ranges.items():
        start = (params['start'])
        end = (params['end'])

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
        
        x_result = x[start:end]
        x_result = x_result - np.min(x_result)

        range_df = DataFrame({'Amp': x_result, 'time': y[start:end]})
        extra_data.extend([
            ResultData(
                main_data = range_df,
                type = f'Диапазон {row_idx + 1}',
                view_audio = True
            ),
            ResultData(
                main_data = fourier_spectrum(range_df),
                type = f'Диапазон {row_idx + 1} - Спектр',
            )
        ])

        if row_idx not in f_values:
            message = f'Не задана частота в строке {row_idx}'
            if error_message is None:
                error_message = message
            else:
                error_message += '\n' + message
            continue

        freq = f_values[row_idx]

        sample_rate = int(1 / np.mean(np.diff(x)))
        dt = 1 / sample_rate

        extra_data.extend([
            ResultData(
                main_data = get_filtered_data_f(
                    FilterType.lpf, range_df, dt, m, Fc_up=freq['f0']
                ),
                type = f'Диапазон {row_idx + 1} - Основной тон',
                view_audio=True
            ),
            ResultData(
                main_data = get_filtered_data_f(
                    FilterType.bpf, range_df, dt, m, freq['f1'] - 50, freq['f1'] + 50
                ),
                type = f'Диапазон {row_idx + 1} - Первая форманта',
                view_audio=True
            ),
            ResultData(
                main_data = get_filtered_data_f(
                    FilterType.bpf, range_df, dt, m, freq['f2'] - 50, freq['f2'] + 50
                ),
                type = f'Диапазон {row_idx + 1} - Вторая форманта',
                view_audio=True
            ),
            ResultData(
                main_data = get_filtered_data_f(
                    FilterType.bpf, range_df, dt, m, freq['f3'] - 50, freq['f3'] + 50
                ),
                type = f'Диапазон {row_idx + 1} - Третья форманта',
                view_audio=True
            ),
            ResultData(
                main_data = get_filtered_data_f(
                    FilterType.hpf, range_df, dt, m, Fc_down=freq['f4']
                ),
                type = f'Диапазон {row_idx + 1} - Четвертая форманта',
                view_audio=True
            )
        ])
            
    return FunctionResult(main_data=data, extra_data=extra_data, error_message=error_message)
