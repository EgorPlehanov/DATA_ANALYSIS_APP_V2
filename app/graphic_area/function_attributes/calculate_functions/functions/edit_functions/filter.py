from ....function_typing import FunctionResult, ResultData
from .add_mult_convol_model import convol_model
from ..analytic_functions.fourier import get_fourier, spectr_fourier

import numpy as np
from pandas import DataFrame


def lpf_reverse(lpw):
    '''Возвращает список в обратном порядке'''
    return lpw[:0:-1] + lpw


def lp_filter(dt, Fc, m):
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


def hp_filter(dt, Fc, m):
    '''Функция для генерации фильтра Высоких Частот'''
    lpw = lpf_reverse(lp_filter(dt, Fc, m))
    hpw = []
    Loper = 2 * m + 1
    for k in range(Loper):
        if k == m:
            hpw.append(1 - lpw[k])
        else:
            hpw.append(- lpw[k])
    return hpw


def bpf_filter(dt, Fc1, Fc2, m):
    '''Функция для генерации Полосового Фильтра'''
    lpw1 = lpf_reverse(lp_filter(dt, Fc1, m))
    lpw2 = lpf_reverse(lp_filter(dt, Fc2, m))
    bpw = []
    Loper = 2 * m + 1
    for k in range(Loper):
        bpw.append(lpw2[k] - lpw1[k])
    return bpw


def bs_filter(dt, Fc1, Fc2, m):
    '''Функция для генерации Режекторного Фильтра'''
    bsw = []
    lpw1 = lpf_reverse(lp_filter(dt, Fc1, m))
    lpw2 = lpf_reverse(lp_filter(dt, Fc2, m))
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
    return DataFrame({
        'Amp': np.arange(0, len(spectrum) // 2),
        'f': np.abs(spectrum[: len(spectrum) // 2])
    })


def convolution(x, h, N, M):
    '''Расчет свертки'''
    return [sum(x[i - j] * h[j] for j in range(M) if i - j >= 0) for i in range(N)]


def lpf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc: float,          # Граничное значение
    m: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Фильтра Низких Частот (ФНЧ)
    '''
    lpw = lpf_reverse(lp_filter(dt, Fc, m))
    filter = DataFrame({'x': np.arange(0, len(lpw)), 'y': lpw})

    M = 2 * m + 1
    filter_freq = frequency_response(lpw, M)
    data_len = len(filter_freq) // 2
    filter_spectr = ResultData(
        main_data=DataFrame({'Amp': np.arange(0, data_len), 'f': filter_freq[: data_len]}),
        type='Частотный спектр ФНЧ',
    )
    if data is None:
        return FunctionResult(main_data=filter, extra_data=filter_spectr)
    
    y_values = data.iloc[:, 1].copy()
    extra_data = [filter_spectr]

    extra_data.append(ResultData(
        main_data=fourier_spectrum(data),
        type='Cпектр исходного сигнала',
    ))

    convolve_data = convolution(y_values, lpw, len(y_values), M)
    filtered_data = DataFrame({'x': np.arange(0, len(convolve_data)), 'y': convolve_data})
    
    extra_data.append(ResultData(
        main_data=fourier_spectrum(filtered_data),
        type='Cпектр отфильтрованного сигнала',
    ))

    return FunctionResult(main_data=filtered_data, extra_data=extra_data)


def hpf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc: float,          # Граничное значение               
    m: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Фильтра Высоких Частот (ФВЧ)
    '''
    hpw = hp_filter(dt, Fc, m)
    filter = DataFrame({'x': np.arange(0, len(hpw)), 'y': hpw})

    M = 2 * m + 1
    filter_freq = frequency_response(hpw, M)
    data_len = len(filter_freq) // 2
    filter_spectr = ResultData(
        main_data=DataFrame({'Amp': np.arange(0, data_len), 'f': filter_freq[: data_len]}),
        type='Частотный спектр ФВЧ',
    )
    if data is None:
        return FunctionResult(main_data=filter, extra_data=filter_spectr)
    
    y_values = data.iloc[:, 1].copy()
    extra_data = [filter_spectr]

    extra_data.append(ResultData(
        main_data=fourier_spectrum(data),
        type='Cпектр исходного сигнала',
    ))

    convolve_data = convolution(y_values, hpw, len(y_values), M)
    filtered_data = DataFrame({'x': np.arange(0, len(convolve_data)), 'y': convolve_data})
    
    extra_data.append(ResultData(
        main_data=fourier_spectrum(filtered_data),
        type='Cпектр отфильтрованного сигнала',
    ))

    return FunctionResult(main_data=filtered_data, extra_data=extra_data)


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
    bpw = bpf_filter(dt, Fc1, Fc2, m)
    filter = DataFrame({'x': np.arange(0, len(bpw)), 'y': bpw})
    
    M = 2 * m + 1
    filter_freq = frequency_response(bpw, M)
    data_len = len(filter_freq) // 2
    filter_spectr = ResultData(
        main_data=DataFrame({'Amp': np.arange(0, data_len), 'f': filter_freq[: data_len]}),
        type='Частотный спектр ПФ',
    )
    if data is None:
        return FunctionResult(main_data=filter, extra_data=filter_spectr)
    
    y_values = data.iloc[:, 1].copy()
    extra_data = [filter_spectr]

    extra_data.append(ResultData(
        main_data=fourier_spectrum(data),
        type='Cпектр исходного сигнала',
    ))

    convolve_data = convolution(y_values, bpw, len(y_values), M)
    filtered_data = DataFrame({'x': np.arange(0, len(convolve_data)), 'y': convolve_data})
    
    extra_data.append(ResultData(
        main_data=fourier_spectrum(filtered_data),
        type='Cпектр отфильтрованного сигнала',
    ))

    return FunctionResult(main_data=filtered_data, extra_data=extra_data)


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
    bsw = bs_filter(dt, Fc1, Fc2, m)
    filter = DataFrame({'x': np.arange(0, len(bsw)), 'y': bsw})
    
    M = 2 * m + 1
    filter_freq = frequency_response(bsw, M)
    data_len = len(filter_freq) // 2
    filter_spectr = ResultData(
        main_data=DataFrame({'Amp': np.arange(0, data_len), 'f': filter_freq[: data_len]}),
        type='Частотный спектр РФ',
    )
    if data is None:
        return FunctionResult(main_data=filter, extra_data=filter_spectr)
    
    y_values = data.iloc[:, 1].copy()
    extra_data = [filter_spectr]

    extra_data.append(ResultData(
        main_data=fourier_spectrum(data),
        type='Cпектр исходного сигнала',
    ))

    convolve_data = convolution(y_values, bsw, len(y_values), M)
    filtered_data = DataFrame({'x': np.arange(0, len(convolve_data)), 'y': convolve_data})
    
    extra_data.append(ResultData(
        main_data=fourier_spectrum(filtered_data),
        type='Cпектр отфильтрованного сигнала',
    ))

    return FunctionResult(main_data=filtered_data, extra_data=extra_data)
