from dataclasses import dataclass
from typing import Callable, Dict, Literal, Any
from functools import partial

from ..function_typing import *
from functions import *
from ..view_function.function_parameters import *


@dataclass
class FunctionConfig:
    name: str
    type: Literal['data', 'edit', 'analytic']
    function: Callable
    parameters: Dict[str, Any]

    def __post_init__(self):
        if  isinstance(self.type, str) or self.type not in ['data', 'edit', 'analytic']:
            raise ValueError("Invalid type")



class FunctionLibrary:

    @staticmethod
    def get_function_config_by_name(name: str):
        '''Возвращает конфигурацию функции по ее имени'''
        return FunctionLibrary.function_by_code[name]


    @staticmethod
    def get_function_config_attribut_by_funcname_atribute(
        name: str,
        attribute: Literal['name', 'type', 'function', 'parameters']
    ):
        '''Возвращает аттрибут конфигурации функции по ее имени и названию атрибута'''
        function_config = FunctionLibrary.function_by_code[name]
        return getattr(function_config, attribute)
    

    @staticmethod
    def get_functions_by_type(type: Literal['data', 'edit', 'analytic']):
        '''Возвращает список функций определенного типа'''
        return [
            function_config
            for function_config in FunctionLibrary.function_by_code.values()
            if function_config.type == type
        ]


    function_by_code = {
        "trend": FunctionConfig(
            name="Тренд",
            type="data",
            function=trend,
            params={
                # "type": {
                #     'type': Dropdown,
                #     'title': "Тип тренда",
                #     'options': [
                #         DDOptionItem("linear_rising", "Линейный возрастающий"),
                #         DDOptionItem("linear_falling", "Линейный убывающий"),
                #         DDOptionItem("nonlinear_rising", "Нелинейный возрастающий"),
                #         DDOptionItem("nonlinear_falling", "Нелинейный убывающий"),
                #     ],
                # },
                # "a": Slider(
                #     title="Коэффициент a",
                #     min=0.01,
                #     max=100,
                #     step=0.01,
                #     default_value=0.01,
                # ),
                # 'b': Slider(
                #     title="Коэффициент b",
                #     min=0.1,
                #     max=10.0,
                #     step=0.1,
                #     default_value=0.1,
                # ),
                # 'step': Slider(
                #     title="Шаг по оси X (step)",
                #     min=0.0001,
                #     max=10,
                #     step=0.0001,
                #     default_value=1,
                # ),
                # 'N': Slider(
                #     title="Длина данных (N)",
                #     value_type='int_number',
                #     round_digits=0,
                #     min=100,
                #     max=5000,
                #     step=100,
                #     default_value=1000,
                # ),
                'show_table_data': SwitchEditor()
            }
        )
    }

   

