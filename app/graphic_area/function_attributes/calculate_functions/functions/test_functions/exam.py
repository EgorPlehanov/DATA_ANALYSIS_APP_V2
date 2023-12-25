from ....function_typing import FunctionResult, ResultData, File

from ..edit_functions.filter import *
from ..data_functions.download import read_data
from ..edit_functions.anti_trend import anti_trend_linear

from typing import Dict
import numpy as np
import pandas as pd
from pandas import DataFrame
from functools import partial



def speach_process(
    library_data: File, # Файл с данными
) -> FunctionResult:
    """
    Экзамен
    """
    if library_data is None:
        return FunctionResult()
    
    data = read_data(library_data.path).main_data
    
    extra_data = []

    # удаление линейного тренда
    non_liner_df = anti_trend_linear(data)
    extra_data.append(ResultData(
        type = 'non_liner',
        main_data = non_liner_df
    ))

    # Спектр Фурье


    # Фильтрация
    filter = get_filtered_data(
        type = FilterType.lpf,

    )




    return FunctionResult(
        main_data = data,
        extra_data = extra_data
    )
