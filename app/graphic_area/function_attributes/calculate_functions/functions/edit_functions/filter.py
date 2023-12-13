from ....function_typing import FunctionResult, ResultData

import numpy as np
from pandas import DataFrame


def lpf_reverse(lpw):
    return lpw[:0:-1] + lpw


def lp_filter(dt, Fc, M):
    fact = Fc * dt
    lpw = []
    lpw.append(fact)
    arg = fact * np.pi

    for i in range(1, M + 1):
        lpw.append(np.sin(arg * i) / (np.pi * i))

    lpw[M] = lpw[M] / 2
    sumg = lpw[0]

    d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
    for i in range(1, M + 1):
        sum = d[0]
        arg = np.pi * i / M

        for k in range(1, 4):
            sum += 2 * d[k] * np.cos(arg * k)

        lpw[i] = lpw[i] * sum
        sumg += 2 * lpw[i]
        
    for i in range(M + 1):
        lpw[i] = lpw[i] / sumg
    return lpw


def lpf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc: float,          # Граничное значение
    M: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Фильтра Низких Частот (ФНЧ)
    '''
    if data is None:
        return FunctionResult()
    
    extra_data = []

    y_values = data.iloc[:, 1].copy()
    
    lpw = lp_filter(dt, Fc, M)

    filtered_data = DataFrame({'x': np.arange(0, len(lpw)), 'y': lpw})
    return FunctionResult(main_data=filtered_data, extra_data=extra_data)


def hpf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc: float,          # Граничное значение               
    M: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Фильтра Высоких Частот (ФВЧ)
    '''
    if data is None:
        return FunctionResult()
    
    extra_data = []

    lpw = lpf_reverse(lp_filter(dt, Fc, M))
    hpw = []
    Loper = 2 * M + 1
    for k in range(Loper):
        if k == M:
            hpw.append(1 - lpw[k])
        else:
            hpw.append(- lpw[k])

    filtered_data = DataFrame({'x': np.arange(0, len(hpw)), 'y': hpw})
    return FunctionResult(main_data=filtered_data, extra_data=extra_data)


def bpf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc1: float,         # Нижняя граница
    Fc2: float,         # Верхняя граница
    M: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Полосовой Фильтр (ПФ)
    '''
    if data is None:
        return FunctionResult()
    
    extra_data = []

    lpw1 = lpf_reverse(lp_filter(dt, Fc1, M))
    lpw2 = lpf_reverse(lp_filter(dt, Fc2, M))
    bpw = []
    Loper = 2 * M + 1
    for k in range(Loper):
        bpw.append(lpw2[k] - lpw1[k])

    filtered_data = DataFrame({'x': np.arange(0, len(bpw)), 'y': bpw})
    return FunctionResult(main_data=filtered_data, extra_data=extra_data)


def bsf(
    data: DataFrame,    # Набор данных (из другой функции)
    dt: float,          # 
    Fc1: float,         # Нижняя граница
    Fc2: float,         # Верхняя граница
    M: int              # Ширина окна Поттера
) -> FunctionResult:
    '''
    Режекторный Фильтр (РФ)
    '''
    if data is None:
        return FunctionResult()
    
    extra_data = []

    bsw = []
    lpw1 = lpf_reverse(lp_filter(dt, Fc1, M))
    lpw2 = lpf_reverse(lp_filter(dt, Fc2, M))
    Loper = 2 * M + 1
    for k in range(0, Loper):
        if k == M:
            bsw.append(1. + lpw1[k] - lpw2[k])
        else:
            bsw.append(lpw1[k] - lpw2[k])

    filtered_data = DataFrame({'x': np.arange(0, len(bsw)), 'y': bsw})
    return FunctionResult(main_data=filtered_data, extra_data=extra_data)













# @staticmethod
# def lpf_reverse(lpw):
#     return lpw[:0:-1] + lpw

# @staticmethod
# def hpf(fc, m, dt):
#     lpw = Proccessing.lpf_reverse(Proccessing.lpf(fc, m, dt))
#     hpw = []
#     Loper = 2 * m + 1
#     for k in range(Loper):
#         if k == m:
#             hpw.append(1 - lpw[k])
#         else:
#             hpw.append(- lpw[k])
#     return hpw

# @staticmethod
# def bpf(fc1, fc2, m, dt):
#     lpw1 = Proccessing.lpf_reverse(Proccessing.lpf(fc1, m, dt))
#     lpw2 = Proccessing.lpf_reverse(Proccessing.lpf(fc2, m, dt))
#     bpw = []
#     Loper = 2 * m + 1
#     for k in range(Loper):
#         bpw.append(lpw2[k] - lpw1[k])
#     return bpw

# @staticmethod
# def bsf(fc1, fc2, m, dt):
#     bsw = []
#     lpw1 = Proccessing.lpf_reverse(Proccessing.lpf(fc1, m, dt))
#     lpw2 = Proccessing.lpf_reverse(Proccessing.lpf(fc2, m, dt))
#     Loper = 2 * m + 1
#     for k in range(0, Loper):
#         if k == m:
#             bsw.append(1. + lpw1[k] - lpw2[k])
#         else:
#             bsw.append(lpw1[k] - lpw2[k])
#     return bsw

# @staticmethod
# def frequencyResponse(data, N):
#     out_data = []
#     for i in range(N):
#         out_data.append(data[i] * N)
#     return out_data
    
