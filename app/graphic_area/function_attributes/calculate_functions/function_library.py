from collections import defaultdict
from typing import Literal, Any, Dict

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
    def get_dict_functions_configs() -> Dict[str, FunctionConfig]:
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
    ) -> Any:
        '''Возвращает аттрибут конфигурации функции по ее имени и названию атрибута'''
        function_config = FunctionLibrary.get_function_config_by_key(key)
        return getattr(function_config, attribute)
    

    @staticmethod
    def get_functions_by_type(type: FunctionType) -> list[FunctionConfig]:
        '''Возвращает список функций определенного типа'''
        return [
            function_config
            for function_config in FunctionLibrary.function_by_key.values()
            if function_config.type == type
        ]
    

    @staticmethod
    def get_function_config_parameters_default_values_by_key(key: str) -> Dict[str, Any]:
        '''Возвращает параметры функции по ее имени'''
        function_config = FunctionLibrary.get_function_config_by_key(key)
        return {
            parameter.name: parameter.default_value
            for parameter in function_config.parameters
        }


    function_by_key = {
        'test': FunctionConfig(
            key = "test",
            name = "Тест",
            type = FunctionType.EDIT,
            function = lambda cb, ddfd, dd, fp, sl, sw, tfdt, tf: print('Тестовая печать Тест test()'),
            parameters = [
                CBConfig(
                    name='cb',
                    title='Кнопка',
                    checkboxes=[
                        CBItem(key='cb1', label='Кнопка 1'),
                        CBItem('cb2', 'Кнопка 2'),
                    ],
                    default_value=['cb1']
                ),
                DDFDConfig(
                    name='ddfd',
                    title='Выпадающий список данных из другой функции',
                ),
                DDConfig(
                    name='dd',
                    title='Выпадающий список',
                    options=[
                        DDOptionItem(key='dd1', text='Заначение 1'),
                        DDOptionItem(key='dd2', text='Заначение 2'),
                    ],
                    default_value='dd1'
                ),
                FPConfig(
                    name='fp',
                    title='Выбор файла',
                    button_text='Выбрать файл',
                    settings=FPSettings(),
                    default_value=None
                ),
                SLConfig(
                    name='sl',
                    title='Слайдер',
                    min=0,
                    max=100,
                    step=1,
                    default_value=50
                ),
                SWConfig(
                    name='sw',
                    title='Свитч',
                    default_value=False
                ),
                TFDTConfig(
                    name='tfdt',
                    title='Таблица данных',
                    columns=[
                        TFDTColumn(
                            name='column1',
                            tooltip='Колонка 1',
                            value_type=ValueType.FLOAT
                        ),
                        TFDTColumn('column2', 'Колонка 2', ValueType.INT)
                    ],
                    default_value = [
                        TFDTItem(column_name='column1', row_index=0, value=1),
                        TFDTItem('column2', 0, 2),
                        TFDTItem('column2', 2, 2)
                    ]
                ),
                TFConfig(
                    name='tf',
                    value_type = ValueType.FUNCTION,
                    label = 'lable Функция',
                    prefix_text = 'pref Функция: ',
                    hint_text = 'hint Функция',
                    helper_text = 'help Функция',
                    autocorrect = False,
                    default_value = 'x**2'
                )
            ],
        ),

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
                SLConfig(
                    name='a', title='Параметр a',
                    min=0.01, max=100, step=0.01, default_value=0.01
                ),
                SLConfig(
                    name='b', title='Параметр b',
                    min=0.1, max=10, step=0.1, default_value=1
                ),
                SLConfig(
                    name='step', title='Шаг по оси X (step)',
                    min=0.0001, max=10, step=1, default_value=1,
                    value_type=ValueType.FLOAT, round_digits=4
                ),
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=100, max=5000, step=100, default_value=1000,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        )
    }

   

