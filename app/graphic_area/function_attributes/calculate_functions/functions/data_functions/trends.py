from ....function_typing import FunctionResult

from typing import List
import numpy as np
import pandas as pd
from enum import Enum


class TrendType(Enum):
    '''Тип тренда'''
    LINEAR_RISING = 'linear_rising'
    LINEAR_FALLING = 'linear_falling'
    NONLINEAR_RISING = 'nonlinear_rising'
    NONLINEAR_FALLING = 'nonlinear_falling'

    def __str__(self):
        return self.value


trend_type_to_function = {
    # Возвращает функцию тренда по типу
    TrendType.LINEAR_RISING:     lambda t, a, b: a * t + b,          # Линейно восходящий
    TrendType.LINEAR_FALLING:    lambda t, a, b: -a * t + b,         # Линейно нисходящий
    TrendType.NONLINEAR_RISING:  lambda t, a, b: b * np.exp(a * t),  # Нелинейно восходящий
    TrendType.NONLINEAR_FALLING: lambda t, a, b: b * np.exp(-a * t), # Нелинейно нисходящий
}


def trend(
    type: TrendType,    # Тип тренда
    a: float,           # Коэффициент a
    b: float,           # Коэффициент b
    step: float,        # Шаг генерации данных
    N: int              # Длина данных
) -> FunctionResult:
    '''
    Создает графики тренда
    '''
    t = np.arange(0, N * step, step)

    if type not in trend_type_to_function:
        raise ValueError(f"Тип {type} не поддерживается")

    data = trend_type_to_function[type](t, a, b)
    trend_data = pd.DataFrame({'x': t, 'y': data})
    return FunctionResult(main_data=trend_data)


# def multi_trend(
#     type_list: list,  # Список типов функций тренда
#     a: float,         # Коэффициент a
#     b: float,         # Коэффициент b
#     step: float,      # Шаг генерации данных
#     N: int,           # Длина данных
# ) -> FunctionResult:
#     ''' Создает графики нескольких функций тренда'''
#     if len(type_list) == 0:
#         raise ValueError("Нет данных для построения графика")
    
#     df_list = []
#     for type in type_list:
#         df_list.append(trend(type, a, b, step, N))
#     return df_list


def combinate_trend(
    type_list: List[TrendType], # Список типов функций тренда
    a: float,       # Коэффициент a
    b: float,       # Коэффициент b
    step: float,    # Шаг генерации данных
    N: int          # Длина данных
) -> FunctionResult:
    '''
    Создает график комбинированной функции тренда
    '''
    num_parts = len(type_list)
    if num_parts == 0:
        raise ValueError("Выберите хотя бы один тип тренда для построения графика")

    # Разделить период t на равные части
    t_parts = np.array_split(np.arange(0, N * step, step), num_parts)

    df_list = []
    previous_end_value = None
    for i, type in enumerate(type_list):
        # Сгенерировать данные для каждой части
        if type not in trend_type_to_function:
            raise ValueError(f"Тип {type} не поддерживается")
        data = trend_type_to_function[type](t_parts[i], a, b)

        # Смещение начала графика до уровня конца предыдущей части
        if previous_end_value is not None:
            shift = previous_end_value - data[0]
            data = [value + shift for value in data]

        df_list.append(pd.DataFrame({'x': t_parts[i], 'y': data}))

        # Обновите значение последнего элемента для следующей итерации
        previous_end_value = data[-1]
        
    combined_df = pd.concat(df_list, ignore_index=True)
    return FunctionResult(main_data=combined_df)
