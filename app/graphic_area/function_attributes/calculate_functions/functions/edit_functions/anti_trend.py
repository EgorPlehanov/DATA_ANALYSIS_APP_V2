from ....function_typing import FunctionResult

import numpy as np
import pandas as pd
from pandas import DataFrame


def anti_trend_linear(
    data: DataFrame  # Набор данных (из другой функции)
) -> FunctionResult:
    '''
    Убирает линейный тренд
    '''
    if data is None:
        return FunctionResult()
    
    x_values = data.iloc[:, 0].copy()
    y_values = data.iloc[:, 1].copy()

    # Подгонка линейного тренда к данным
    linear_trend = np.polyfit(x_values, y_values, 1)
    linear_fit = np.polyval(linear_trend, x_values)
    
    # Удаление линейного тренда путем вычитания линейной подгонки
    detrended_data = y_values - linear_fit
    
    # Вычисление первой производной (градиента) отдетрендированных данных
    derivative = np.gradient(detrended_data)

    no_linear_df = pd.DataFrame({'x': x_values, 'y': derivative})
    return FunctionResult(main_data=no_linear_df)


def anti_trend_non_linear(
    data: DataFrame, # Набор данных (из другой функции)
    W: int      # Ширина окна
) -> FunctionResult:
    '''
    Убирает нелинейный тренд (метод скользящего среднего)
    '''
    if data is None:
        return FunctionResult()
    
    W = int(W)
    
    y_values = data.iloc[:, 1].copy()
    N = len(y_values) - W
    for n in range(N):
        y_values[n] -= sum(y_values[n:n+W]) / W

    no_non_linear_df = pd.DataFrame({'x': data.iloc[:, 0].copy(), 'y': y_values})
    return FunctionResult(main_data=no_non_linear_df)
