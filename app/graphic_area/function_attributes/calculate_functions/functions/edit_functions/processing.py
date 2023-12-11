from ....function_typing import FunctionResult

import numpy as np
import pandas as pd
from pandas import DataFrame


def scale_values(
    data: DataFrame,    # Набор данных (из другой функции)
    new_min: float,     # Новое минимальное значение
    new_max: float      # Новое максимальное значение
) -> FunctionResult:
    '''
    Нормирование значений
    '''
    if data is None:
        return FunctionResult()
    
    y_values = data.iloc[:, 1].copy()

    min_val = np.min(y_values)
    max_val = np.max(y_values)
    
    normalized = new_min + ((y_values - min_val) * (new_max - new_min)) / (max_val - min_val)

    scale_df = DataFrame({'x': data.iloc[:, 0].copy(), 'y': normalized})
    return FunctionResult(main_data=scale_df)
    

def normalize_values(
    data: DataFrame,    # Набор данных (из другой функции)
    new_max: float      # Новое максимальное значение (по модулю [-new_max, new_max])
) -> FunctionResult:
    '''
    Нормализация значений
    '''
    if data is None:
        return FunctionResult()
    
    y_values = data.iloc[:, 1].copy()

    max_val = np.max(y_values)
    
    normalized = y_values / max_val * new_max

    normalize_df = pd.DataFrame({'x': data.iloc[:, 0].copy(), 'y': normalized})
    return FunctionResult(main_data=normalize_df)


def absolute_value(
    data: DataFrame,    # Набор данных (из другой функции)
) -> FunctionResult:
    '''
    Абсолютное значение
    '''
    if data is None:
        return FunctionResult()
    
    y_values = data.get('y').copy()

    absolute_df = pd.DataFrame({'x': data.get('x').copy(), 'y': np.abs(y_values)})
    return FunctionResult(main_data=absolute_df)