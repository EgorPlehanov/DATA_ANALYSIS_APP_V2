# from dataclasses import dataclass
# from typing import Callable, Dict, Literal
# from .function_typing import *
# import numpy as np
# import pandas as pd
# from functools import partial




# @dataclass
# class FunctionConfig:
#     name: str
#     type: Literal['data', 'edit', 'analytic']
#     function: Callable
#     parameters: Dict[str, Any]

#     def __post_init__(self):
#         if  isinstance(self.type, str) or self.type not in ['data', 'edit', 'analytic']:
#             raise ValueError("Invalid type")




# def trend(type: str, a: float, b: float, step: float, N: int) -> list:    
#     trend_type_to_function = {
#     "linear_rising": lambda t, a, b: a * t + b,
#         "linear_falling": lambda t, a, b: -a * t + b,
#         "nonlinear_rising": lambda t, a, b: b * np.exp(a * t),
#         "nonlinear_falling": lambda t, a, b: b * np.exp(-a * t),
#     }

#     t = np.arange(0, N * step, step)

#     data = None
#     if type in trend_type_to_function:
#         data = trend_type_to_function[type](t, a, b)

#     df = pd.DataFrame({'x': t, 'y': data})
#     return df




# class FunctionLibrary:

#     function_by_code = {
#         "trend": FunctionConfig(
#             name="trend",
#             type="data",
#             function=trend,
#             params={
#                 "type": {
#                     'type': Dropdown,
#                     'title': "Тип тренда",
#                     'options': [
#                         DDOptionItem("linear_rising", "Линейный возрастающий"),
#                         DDOptionItem("linear_falling", "Линейный убывающий"),
#                         DDOptionItem("nonlinear_rising", "Нелинейный возрастающий"),
#                         DDOptionItem("nonlinear_falling", "Нелинейный убывающий"),
#                     ],
#                 },
#                 "a": Slider(
#                     title="Коэффициент a",
#                     min=0.01,
#                     max=100,
#                     step=0.01,
#                     default_value=0.01,
#                 ),
#                 'b': Slider(
#                     title="Коэффициент b",
#                     min=0.1,
#                     max=10.0,
#                     step=0.1,
#                     default_value=0.1,
#                 ),
#                 'step': Slider(
#                     title="Шаг по оси X (step)",
#                     min=0.0001,
#                     max=10,
#                     step=0.0001,
#                     default_value=1,
#                 ),
#                 'N': Slider(
#                     title="Длина данных (N)",
#                     value_type='int_number',
#                     round_digits=0,
#                     min=100,
#                     max=5000,
#                     step=100,
#                     default_value=1000,
#                 ),
#                 'show_table_data': Switch()
#             }
#         )
#     }

#     @staticmethod
#     def get_function_by_name(name: str):
#         function_config = FunctionLibrary.function_by_code[name]

