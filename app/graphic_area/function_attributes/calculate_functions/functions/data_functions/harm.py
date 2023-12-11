from ....function_typing import FunctionResult

from typing import Dict
import numpy as np
import pandas as pd


def harm(
    N: int,         # Длина данных
    A0: float,      # Амплитуда
    f0: float,      # Частота
    delta_t: float  # Шаг генерации данных
) -> FunctionResult:
    '''
    Создает гармонический процесс
    '''
    error_message = None
    if delta_t > 1 / (2 * f0):
        error_message = "Некоректное значение временного интервала, delta_t <= 1/(2*f0): " \
            + f"delta_t = {delta_t}, 1/(2*f0) = {round(1 / (2 * f0), 5)}"

    k = np.arange(0, N)
    y_values = A0 * np.sin(2 * np.pi * f0 * delta_t * k)

    harm_data = pd.DataFrame({'x': delta_t * k, 'y': y_values})
    return FunctionResult(main_data=harm_data, error_message=error_message)


def poly_harm(
    N: int,         # Длина данных
    A_f_data: Dict, # Список Амплитуд и Частот
    delta_t: float  # Шаг генерации данных
) -> list:
    '''
    Создает полигормонический процесс
    '''
    if len(A_f_data) == 0:
        raise ValueError("Нет данных об амплитуде и частоте для построения графика")

    max_fi = max([params['f'] for params in A_f_data.values()])
    error_message = None
    if delta_t > 1 / (2 * max_fi):
        error_message = "Некоректное значение временного интервала.\nОно должно удовлетворять условию: " \
            + f"delta_t <= 1 / (2 * max(fi)): delta_t = {delta_t}," \
            + f"1 / (2 * max(fi)) = {round(1 / (2 * max_fi), 5)}"

    # N = int(N)
    k = np.arange(0, N)
    y_values = np.zeros(N)
    for params in A_f_data.values():
        y_values += params['A'] * np.sin(2 * np.pi * params['f'] * delta_t * k)

    poly_harm_data = pd.DataFrame({'x': delta_t * k, 'y': y_values})
    return FunctionResult(main_data=poly_harm_data, error_message=error_message)
