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
            type = FunctionType.DATA,
            function = lambda cb, ddfd, dd, fp, sl, sw, tfdt, tf: FunctionResult(None, None, None),
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
                    round_digits=4
                ),
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=100, max=5000, step=100, default_value=1000,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        ),

        # 'multi_trend': FunctionConfig(
        #     key = 'multi_trend',
        #     name = 'Мультитренд',
        #     type = FunctionType.DATA,
        #     function = multi_trend,
        #     parameters = [
        #         CBConfig(
        #             name='type_list',
        #             title='Тип тренда',
        #             checkboxes=[
        #                 CBItem('linear_rising', 'Линейно восходящий'),
        #                 CBItem('linear_falling', 'Линейно нисходящий'),
        #                 CBItem('nonlinear_rising', 'Нелинейно восходящий'),
        #                 CBItem('nonlinear_falling', 'Нелинейно нисходящий'),
        #             ],
        #             default_value=['linear_rising', 'linear_falling', 'nonlinear_rising', 'nonlinear_falling']
        #         ),
        #         SLConfig(
        #             name='a', title='Параметр a',
        #             min=0.01, max=10, step=0.01, default_value=0.01
        #         ),
        #         SLConfig(
        #             name='b', title='Параметр b',
        #             min=0.1, max=10, step=0.1, default_value=1
        #         ),
        #         SLConfig(
        #             name='step', title='Шаг по оси X (step)',
        #             min=1, max=15, step=1, default_value=1,
        #         ),
        #         SLConfig(
        #             name='N', title='Длина данных (N)',
        #             min=100, max=5000, step=100, default_value=1000,
        #             value_type=ValueType.INT, round_digits=0
        #         ),
        #         SWConfig(),
        #     ]
        # ),

        'combinate_trend': FunctionConfig(
            key = 'combinate_trend',
            name = 'Кусочная функция',
            type = FunctionType.DATA,
            function = combinate_trend,
            parameters = [
                CBConfig(
                    name='type_list',
                    title='Тип тренда',
                    checkboxes=[
                        CBItem('linear_rising', 'Линейно восходящий'),
                        CBItem('linear_falling', 'Линейно нисходящий'),
                        CBItem('nonlinear_rising', 'Нелинейно восходящий'),
                        CBItem('nonlinear_falling', 'Нелинейно нисходящий'),
                    ],
                    default_value=['linear_rising', 'linear_falling', 'nonlinear_rising', 'nonlinear_falling']
                ),
                SLConfig(
                    name='a', title='Параметр a',
                    min=0.01, max=10, step=0.01, default_value=0.01
                ),
                SLConfig(
                    name='b', title='Параметр b',
                    min=0.1, max=10, step=0.1, default_value=1
                ),
                SLConfig(
                    name='step', title='Шаг по оси X (step)',
                    min=1, max=15, step=1, default_value=1,
                ),
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=100, max=5000, step=100, default_value=1000,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        ),

        
    }

   

# ======================================================================================
# ======================================================================================


functions_info = {

    'combinate_trend': {
        # 'function': DataFunctions.combinate_trend,
        'type': 'data',
        'name': 'Кусочная функция',
        'parameters': {
            "type_list": {
                "type": "checkbox",
                "title": "Тип тренда",
                "checkboxes": [
                    {
                        "key": "linear_rising",
                        "label": "Линейно восходящий",
                        'default_value': True,
                    },
                    {
                        "key": "linear_falling",
                        "label": "Линейно нисходящий",
                        'default_value': True,
                    },
                    {
                        "key": "nonlinear_rising",
                        "label": "Нелинейно восходящий",
                        'default_value': True,
                    },
                    {
                        "key": "nonlinear_falling",
                        "label": "Нелинейно нисходящий",
                        'default_value': True,
                    }
                ],
                "default_value": ["nonlinear_rising", "nonlinear_falling", "linear_rising", "linear_falling"],
            },
            "a": {
                "type": "slider",
                "title": "Параметр (a)",
                "min": 0.01,
                "max": 10.0,
                "step": 0.01,
                "default_value": 0.01,
            },
            "b": {
                "type": "slider",
                "title": "Параметр (b)",
                "min": 0.1,
                "max": 10.0,
                "step": 0.1,
                "default_value": 1.0,
            },
            "step": {
                "type": "slider",
                "title": "Шаг по оси x (step)",
                "min": 1,
                "max": 15,
                "step": 1,
                "default_value": 1,
            },
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 100,
                'round_digits': 0,
                "default_value": 600,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'harm': {
        # 'function': DataFunctions.harm,
        'type': 'data',
        'name': 'Гармонический процесс',
        'parameters': {
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 10,
                'round_digits': 0,
                "default_value": 1024,
            },
            "A0": {
                "type": "slider",
                "title": "Амплитуда (A0)",
                "min": 1,
                "max": 1000,
                "step": 1,
                "default_value": 100,
            },
            "f0": {
                "type": "slider",
                "title": "Частота (f0), Гц",
                "min": 1,
                "max": 1000,
                "step": 1,
                "default_value": 15,
            },
            "delta_t": {
                "type": "slider",
                "title": "Временной интервал (delta_t)",
                "min": 0.0001,
                "max": 0.01,
                "step": 0.0001,
                "round_digits": 5,
                "default_value": 0.0001,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'poly_harm': {
        # 'function': DataFunctions.poly_harm,
        'type': 'data',
        'name': 'Полигармонический процесс',
        'parameters': {
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 10,
                'round_digits': 0,
                "default_value": 1000,
            },
            "A_f_data": {
                "type": "textfields_datatable",
                "title": "Амплитуда (A) и частота (f)",
                "columns": {
                    "A": {
                        'name': 'A',
                        'tooltip': 'Амплитуда гармонического процесса',
                    },
                    "f": {
                        'name': 'f, Гц',
                        'tooltip': 'Частота гармонического процесса в герцах (Гц)'
                    },
                },
                "default_value": {
                    0: {"A": 100, "f": 33},
                    1: {"A": 15, "f": 5},
                    2: {"A": 20, "f": 170},
                },
            },
            "delta_t": {
                "type": "slider",
                "title": "Временной интервал (delta_t)",
                "min": 0.0001,
                "max": 0.01,
                "step": 0.0001,
                "round_digits": 5,
                "default_value": 0.0001,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'custom_function': {
        # 'function': DataFunctions.custom_function,
        'type': 'data',
        'name': 'Задать свою функцию',
        'parameters': {
            'expression': {
                'type': 'text_field',
                'text_type': 'function',
                'label': 'Функция',
                'prefix_text': 'y = ',
                'hint_text': 'например: 1 + sin(x**2)',
                'helper_text': 'Функция должна содержать только аргумент x',
                'default_value': 'x',
            },
            "N": {
                "type": "slider",
                "title": "Длина данных (N)",
                'text_type': 'int_number',
                "min": 100,
                "max": 5000,
                "step": 100,
                'round_digits': 0,
                "default_value": 600,
            },
            "step": {
                "type": "slider",
                "title": "Шаг по оси x (step)",
                "min": 0.1,
                "max": 10,
                "step": 0.1,
                "default_value": 1,
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },

    'data_download': {
        # 'function': DataFunctions.data_download,
        'type': 'data',
        'name': 'Загрузить свой набор данных',
        'parameters': {
            'input_data': {
                "type": "file_picker",
                "title": "Набор данных",
                'button_text': 'Выбрать набор данных',
                'pick_files_parameters': {
                    'dialog_title': 'Выбор набора данных',
                    'initial_directory': None,
                    'file_type': None,
                    'allowed_extensions': ['csv', 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'txt', 'dat'],
                    'allow_multiple': True,
                },
                "default_value": [],
            },
            'show_table_data': {
                "type": "switch",
                "title": "Показывать таблицу данных?",
                'default_value': False
            },
        }
    },
}