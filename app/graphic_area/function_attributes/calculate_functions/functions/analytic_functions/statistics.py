from ....function_typing import FunctionResult

import numpy as np
from pandas import DataFrame


def statistics(
    data: DataFrame  # Набор данных (из другой функции)
) -> FunctionResult:
    """
    Рассчитывает статистические характеристики данных.
    """
    if data is None:
        return FunctionResult()

    y = data.get('y').copy()

    min_value = np.min(y)
    max_value = np.max(y)
    mean = np.mean(y)
    variance = np.var(y, ddof=1)  # Используем ddof=1 для несмещенной оценки дисперсии
    std_dev = np.sqrt(variance)
    
    # Рассчет асимметрии и коэффициента асимметрии
    mu3 = np.mean((y - mean) ** 3)
    delta3 = np.power(variance, 1.5)
    skewness = mu3 / delta3
    skewness_coeff = skewness / np.power(variance, 1.5)
    
    # Рассчет эксцесса и коэффициента эксцесса
    mu4 = np.mean((y - mean) ** 4)
    kurtosis = mu4 / np.power(variance, 2)
    kurtosis_coeff = kurtosis / (variance ** 2) - 3

    # Рассчет Среднего квадрата и Среднеквадратической ошибки
    squared_mean = np.mean(y ** 2)
    rmse = np.sqrt(variance)

    stats_df = DataFrame({
        'Параметр': [
            'Минимум', 'Максимум', 'Среднее', 'Дисперсия', 'Стандартное отклонение', 'Асимметрия (A)',
            'Коэффициент асимметрии', 'Эксцесс (Э)', 'Куртозис', 'Средний квадрат (СК)', 'Среднеквадратическая ошибка'
        ],
        'Значение': list(map(lambda x: round(x, 5), [
            min_value, max_value, mean, variance, std_dev, skewness,
            skewness_coeff, kurtosis, kurtosis_coeff, squared_mean, rmse
        ]))
    })
    return FunctionResult(main_data=stats_df)


def stationarity(
    data: DataFrame,    # Набор данных (из другой функции)
    M: int              # Количество интервалов
) -> FunctionResult:
    """
    Оценивает стационарность данных.
    """
    if data:
        return FunctionResult()
    
    M = int(M)

    y = data.get('y').copy()
    N = len(y)

    error_message = ''
    if M > N:
        raise ValueError(
            f'Некорректное кол-во интервалов: M должен быть <= N. M = {M}, N = {N}'
        )
    
    y_min = np.min(y)
    if y_min < 0:
        y = y[:] - y_min

    intervals = np.array_split(y, M)
    intervals_means = np.array([np.mean(interval) for interval in intervals])
    intervals_std = np.array([np.std(interval) for interval in intervals])

    df_mean = np.mean(y)
    df_std = np.std(y)

    is_stationarity = True
    for i in range(M):
        if not is_stationarity:
            break

        for j in range(i + 1, M):
            delta_mean = abs(intervals_means[i] - intervals_means[j])
            delta_std_dev = abs(intervals_std[i] - intervals_std[j])

            if (delta_mean / df_mean) > 0.05 or (delta_std_dev / df_std) > 0.05:
                is_stationarity = False
                break

    stats_df = DataFrame({
        'Параметр': ['Стационарность'],
        'Значение': [f"Процесс {'' if is_stationarity else 'НЕ '}стационарный"]
    })
    return FunctionResult(main_data=stats_df)
