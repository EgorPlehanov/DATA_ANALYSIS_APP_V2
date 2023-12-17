from ....function_typing import FunctionResult, ResultData

import numpy as np
import pandas as pd
from pandas import DataFrame


def get_fourier(
    y_values: np.array  # Список значений
) -> DataFrame:
    '''
    Вычисление прямого преобразования Фурье
    '''
    N = len(y_values)
    # Вычисление прямого преобразования Фурье
    real_part = np.zeros(N)  # Для действительной части
    imag_part = np.zeros(N)  # Для мнимой части

    k_values = np.arange(N)
    n_values = np.arange(N)

    cos_values = np.cos(2 * np.pi * np.outer(n_values, k_values) / N)
    sin_values = np.sin(2 * np.pi * np.outer(n_values, k_values) / N)

    real_part = np.dot(y_values, cos_values)
    imag_part = np.dot(y_values, sin_values)

    # Вычисление амплитудного спектра
    X_amp = np.sqrt(real_part ** 2 + imag_part ** 2)
    return DataFrame({'Re[Xn]': real_part, 'Im[Xn]': imag_part, '|Xn|': X_amp})


def fourier(
    data: DataFrame,                    # Набор данных (из другой функции)
    show_calculation_table: bool=False  # Показывать ли таблицу с вычислениями
) -> FunctionResult:
    '''
    Построение прямого преобразования Фурье
    '''
    if data is None:
        return FunctionResult()
    
    y_values = data.iloc[:, 1].copy()
    fourier_data = get_fourier(y_values)

    extra_data = None
    if show_calculation_table:
        extra_data = [ResultData(
            type='fourier',
            main_data=fourier_data,
            view_chart=False,
            view_table_horizontal=True
        )]

    fourier_df = DataFrame({'n': np.arange(len(fourier_data)), '|Xn|': fourier_data['|Xn|']})
    return FunctionResult(main_data=fourier_df, extra_data=extra_data)


def spectr_fourier(
    data: DataFrame,        # Набор данных (из другой функции)
    delta_t: float = None,  # Шаг генерации данных
    L_window: int = 0       # Ширина окна
) -> FunctionResult:
    '''
    Построение амплитудного спектра Фурье на основе прямого преобразования Фурье
    '''
    if data is None:
        return FunctionResult()
    
    L_window = int(L_window)
    
    y_values = data.get('y').copy()
    Xn_values = np.abs(np.fft.fft(
        y_values * np.concatenate([np.ones(len(y_values) - L_window), np.zeros(L_window)])
    ))

    N = len(Xn_values) // 2

    f_border = 1 / (2 * delta_t)
    delta_f = f_border / N
    frequencies = np.arange(N) * delta_f

    spectr_fourier_df = pd.DataFrame({'f': frequencies, '|Xn|': Xn_values[:N]})
    return FunctionResult(main_data=spectr_fourier_df)
