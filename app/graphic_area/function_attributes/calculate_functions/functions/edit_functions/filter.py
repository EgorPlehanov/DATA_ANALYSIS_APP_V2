from ....function_typing import FunctionResult, ResultData

from enum import Enum
import numpy as np
from pandas import DataFrame
from functools import partial


def reverse_and_mirror(lpw):
    '''Функция для развернуть и зеркалить массив'''
    return lpw[:0:-1] + lpw


def lp_values(dt, Fc, m):
    '''Функция для генерации фильтра Низких Частот'''
    fact = 2 * Fc * dt
    lpw = [fact]
    arg = fact * np.pi
    for i in range(1, m + 1):
        lpw.append(np.sin(arg * i) / (np.pi * i))
    lpw[m] = lpw[m] / 2
    sumg = lpw[0]
    d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
    for i in range(1, m + 1):
        sum = d[0]
        arg = np.pi * i / m
        for k in range(1, 4):
            sum += 2 * d[k] * np.cos(arg * k)
        lpw[i] = lpw[i] * sum
        sumg += 2 * lpw[i]
    for i in range(m + 1):
        lpw[i] = lpw[i] / sumg
    return lpw


def lp_filter(dt, Fc, m):
    '''Функция для генерации фильтра Низких Частот'''
    return reverse_and_mirror(lp_values(dt, Fc, m))


def hp_filter(dt, Fc, m):
    '''Функция для генерации фильтра Высоких Частот'''
    lpw = lp_filter(dt, Fc, m)
    hpw = []
    Loper = 2 * m + 1
    for k in range(Loper):
        if k == m:
            hpw.append(1 - lpw[k])
        else:
            hpw.append(- lpw[k])
    return hpw


def bp_filter(dt, Fc1, Fc2, m):
    '''Функция для генерации Полосового Фильтра'''
    lpw1 = lp_filter(dt, Fc1, m)
    lpw2 = lp_filter(dt, Fc2, m)
    bpw = []
    Loper = 2 * m + 1
    for k in range(Loper):
        bpw.append(lpw2[k] - lpw1[k])
    return bpw


def bs_filter(dt, Fc1, Fc2, m):
    '''Функция для генерации Режекторного Фильтра'''
    bsw = []
    lpw1 = lp_filter(dt, Fc1, m)
    lpw2 = lp_filter(dt, Fc2, m)
    Loper = 2 * m + 1
    for k in range(0, Loper):
        if k == m:
            bsw.append(1. + lpw1[k] - lpw2[k])
        else:
            bsw.append(lpw1[k] - lpw2[k])
    return bsw


def fourier_proc(data):
    N = len(data)
    freqs = np.arange(N)
    cos_vals = np.cos(2 * np.pi * np.outer(freqs, freqs) / N)
    sin_vals = np.sin(2 * np.pi * np.outer(freqs, freqs) / N)
    Re_Xn = np.dot(data, cos_vals)
    Im_Xn = np.dot(data, sin_vals)
    Re_Xn /= N
    Im_Xn /= N
    Xn = np.sqrt((Re_Xn**2) + (Im_Xn**2))
    return Xn.tolist()


def frequency_response(filter: list, N: int) -> list:
    '''Расчет частотного сглаживания'''
    return [Xn * N for Xn in fourier_proc(filter)]


def calculate_sample_rate(data: DataFrame) -> float:
    '''Расчет частоты дискретизации'''
    x_values = data.iloc[:, 0].copy()
    time_diff = x_values.iloc[-1] - x_values.iloc[0]
    num_samples = len(data)
    sample_rate = time_diff / num_samples
    return sample_rate


def fourier_spectrum(data: DataFrame) -> DataFrame:
    '''Расчет амплитудного спектра Фурье'''
    y_values = data.iloc[:, 1].copy()
    x_values = data.iloc[:, 0].copy()

    spectrum = np.fft.fft(y_values)
    frequency = np.fft.fftfreq(len(y_values), d=x_values.iloc[1] - x_values.iloc[0])
    print(frequency)
    return DataFrame({
        'Amp': np.arange(0, len(spectrum) // 2),
        'f': np.abs(spectrum[: len(spectrum) // 2])
    })


def convolution(x, h, N, M):
    '''Расчет свертки'''
    return [sum(x[i - j] * h[j] for j in range(M) if i - j >= 0) for i in range(N)]



class FilterType(Enum):
    lpf = 1
    hpf = 2
    bpf = 3
    bsf = 4


def get_filtered_data(
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
    filter = DataFrame({'x': np.arange(0, len(filter_values)), 'y': filter_values})
    
    M = 2 * m + 1
    filter_freq = frequency_response(filter_values, M)
    data_len = len(filter_freq) // 2
    extra_data = [ResultData(
        main_data=DataFrame({'Amp': np.arange(0, data_len), 'f': filter_freq[: data_len]}),
        type='Частотный спектр',
    )]
    if data is None:
        return FunctionResult(main_data=filter, extra_data=extra_data)
    
    y_values = data.iloc[:, 1].copy()
    
    extra_data.append(ResultData(
        main_data=fourier_spectrum(data),
        type='Cпектр исходного сигнала',
    ))

    convolve_data = convolution(y_values, filter_values, len(y_values), M)
    filtered_data = DataFrame({'x': np.arange(0, len(convolve_data)), 'y': convolve_data})
    
    extra_data.append(ResultData(
        main_data=fourier_spectrum(filtered_data),
        type='Cпектр отфильтрованного сигнала',
    ))

    return FunctionResult(main_data=filtered_data, extra_data=extra_data)



def lpf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc: float,          # Граничное значение
    m: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Фильтра Низких Частот (ФНЧ)
    '''
    return get_filtered_data(FilterType.lpf, data, dt, m, Fc_up=Fc)


def hpf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc: float,          # Граничное значение               
    m: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Фильтра Высоких Частот (ФВЧ)
    '''
    return get_filtered_data(FilterType.hpf, data, dt, m, Fc_down=Fc)


def bpf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc1: float,         # Нижняя граница
    Fc2: float,         # Верхняя граница
    m: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Полосовой Фильтр (ПФ)
    '''
    return get_filtered_data(FilterType.bpf, data, dt, m, Fc_down=Fc1, Fc_up=Fc2)


def bsf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc1: float,         # Нижняя граница
    Fc2: float,         # Верхняя граница
    m: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Режекторный Фильтр (РФ)
    '''
    return get_filtered_data(FilterType.bsf, data, dt, m, Fc_down=Fc1, Fc_up=Fc2)
