from ....function_typing import FunctionResult

import numpy as np
import pandas as pd
from pandas import DataFrame


def hist(
    data: DataFrame,            # Набор данных (из другой функции)
    M: int,                     # Количество интервалов
    is_density: bool = True,    # True - строить график плотности, False - гистограмму количества
) -> FunctionResult:
    '''
    Строит графики функции плотности распределения вероятностей
    '''
    if data is None:
        return FunctionResult()
    
    M = int(M)
    
    counts, bin_edges = np.histogram(data.iloc[:, 1].copy(), bins=M, density=is_density)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    axi_name = 'density' if is_density else 'count'
    hist_df = pd.DataFrame({'y': bin_centers, axi_name: counts})
    return FunctionResult(main_data=hist_df)
