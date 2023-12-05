from collections import defaultdict
from typing import Literal, Any

from ..view_function.function_parameters import *
from ..function_typing import *
from .functions import *


class FunctionLibrary:
    @staticmethod
    def get_russian_type_name(type: FunctionType) -> str:
        '''Возвращает русское название типа функции'''
        russian_type_name = {
            FunctionType.DATA: 'Данные',
            FunctionType.EDIT: 'Обработка',
            FunctionType.ANALYTIC: 'Аналитика',
        }
        if type in russian_type_name:
            return russian_type_name[type]
        return type


    @staticmethod
    def get_function_dict() -> dict:
        '''Возвращает словарь функций в виде {'type': [namedtuple(key, name), ...], ...}'''
        grouped_functions = defaultdict(list)
        for function in FunctionLibrary.function_by_key.values():
            function_data = FunctionMenuOption(key=function.key, name=function.name)
            type = FunctionLibrary.get_russian_type_name(function.type)
            grouped_functions[type].append(function_data)
        return grouped_functions


    @staticmethod
    def get_function_config_by_key(key: str) -> FunctionConfig:
        '''Возвращает конфигурацию функции по ее имени'''
        if key not in FunctionLibrary.function_by_key:
            raise ValueError(f'Недопустимое key: {key}')
        return FunctionLibrary.function_by_key[key]


    @staticmethod
    def get_function_config_attribute_by_key_attribute(
        key: str,
        attribute: Literal['name', 'type', 'function', 'parameters']
    ):
        '''Возвращает аттрибут конфигурации функции по ее имени и названию атрибута'''
        function_config = FunctionLibrary.get_function_config_by_key(key)
        return getattr(function_config, attribute)
    

    @staticmethod
    def get_functions_by_type(type: FunctionType):
        '''Возвращает список функций определенного типа'''
        return [
            function_config
            for function_config in FunctionLibrary.function_by_key.values()
            if function_config.type == type
        ]
    

    @staticmethod
    def get_function_config_parameters_default_values_by_key(key: str) -> dict[str, Any]:
        '''Возвращает параметры функции по ее имени'''
        function_config = FunctionLibrary.get_function_config_by_key(key)
        return {
            parameter.name: parameter.default_value
            for parameter in function_config.parameters
        }


    function_by_key = {
        "trend": FunctionConfig(
            key = "trend",
            name = "Тренд",
            type = FunctionType.DATA,
            function = trend,
            parameters = [
                DDConfig(
                    name='type',
                    title='Тип тренда',
                    options=[
                        DDOptionItem(key='linear_rising', text='Линейный восходящий'),
                        DDOptionItem(key='linear_falling', text='Линейный нисходящий'),
                        DDOptionItem(key='nonlinear_rising', text='Нелинейный восходящий'),
                        DDOptionItem(key='nonlinear_falling', text='Нелинейный нисходящий'),
                    ],
                    default_value='linear_rising'
                ),
                SLConfig(name='a'),
                SLConfig(name='b'),
                SLConfig(name='step'),
                SLConfig(name='N'),
                SWConfig(),
            ]
        )
    }

   

