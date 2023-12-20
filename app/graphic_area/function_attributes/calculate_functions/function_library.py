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

        # ================================================
        # FunctionType.DATA
        # ================================================

        'test': FunctionConfig(
            key = "test",
            name = "ТЕСТ",
            type = FunctionType.DATA,
            function = lambda cb, ddfd, dd, fp, sl, sw, tfdt, tf, dl: FunctionResult(None, None, None),
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
                        TFDTColumn('column2', 'Колонка 2', value_type=ValueType.INT)
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
                ),
                DLConfig(
                    name='dl',
                    valid_folders=['dat', 'wav', 'jpg', 'grace', 'rect'],
                    default_value='birches_changed.jpg'#'pgp_2ms.dat'
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

        'harm': FunctionConfig(
            key = 'harm',
            name = 'Гармонический процесс',
            type = FunctionType.DATA,
            function = harm,
            parameters = [
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=100, max=5000, step=100, default_value=1000,
                    value_type=ValueType.INT, round_digits=0
                ),
                SLConfig(
                    name='A0', title='Амплитуда (A0)',
                    min=1, max=1000, step=1, default_value=100
                ),
                SLConfig(
                    name='f0', title='Частота (f0), Гц',
                    min=1, max=1000, step=1, default_value=15
                ),
                SLConfig(
                    name='delta_t', title='Шаг по оси X (delta_t)',
                    min=0.0001, max=0.01, step=0.0001, default_value=0.0001,
                    round_digits=4
                ),
                SWConfig(),
            ]
        ),

        'poly_harm': FunctionConfig(
            key = 'poly_harm',
            name = 'Полигармонический процесс',
            type = FunctionType.DATA,
            function = poly_harm,
            parameters = [
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=100, max=5000, step=10, default_value=1000,
                    value_type=ValueType.INT, round_digits=0
                ),
                TFDTConfig(
                    name='A_f_data', title='Амплитуда (A) и частота (f)',
                    columns=[
                        TFDTColumn(name='A', tooltip='Амплитуда гармонического процесса'),
                        TFDTColumn(name='f', tooltip='Частота гармонического процесса', unit='Гц'),
                    ],
                    default_value=[
                        TFDTItem(column_name='A', row_index=0, value=100),
                        TFDTItem(column_name='f', row_index=0, value=33),
                        TFDTItem(column_name='A', row_index=1, value=15),
                        TFDTItem(column_name='f', row_index=1, value=5),
                        TFDTItem(column_name='A', row_index=2, value=20),
                        TFDTItem(column_name='f', row_index=2, value=170),
                    ]
                ),
                SLConfig(
                    name='delta_t', title='Шаг по оси X (delta_t)',
                    min=0.0001, max=0.01, step=0.0001, default_value=0.0001,
                    round_digits=4
                ),
                SWConfig(),
            ]
        ),

        'custom_function': FunctionConfig(
            key = 'custom_function',
            name = 'Задать свою функцию',
            type = FunctionType.DATA,
            function = custom_function,
            parameters = [
                TFConfig(
                    name='expression',
                    value_type=ValueType.FUNCTION,
                    label='Функция',
                    prefix_text='y = ',
                    hint_text='например: 1 + sin(x**2)',
                    helper_text='Функция должна содержать только аргумент x',
                    default_value='x'
                ),
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=100, max=5000, step=100, default_value=1000,
                    value_type=ValueType.INT, round_digits=0
                ),
                SLConfig(
                    name='step', title='Шаг по оси X (step)',
                    min=0.01, max=10, step=0.1, default_value=1
                ),
                SWConfig(),
            ]
        ),

        'data_download': FunctionConfig(
            key = 'data_download',
            name = 'Загрузить свой набор данных',
            type = FunctionType.DATA,
            function = data_download,
            parameters = [
                FPConfig(name='input_data'),
                SWConfig(),
            ]
        ),

        'data_library': FunctionConfig(
            key = 'data_library',
            name = 'Из библиотеки данных',
            type = FunctionType.DATA,
            function = data_library,
            parameters = [
                DLConfig(valid_folders = ['User_Saved_Data', 'dat', 'wav', 'роза']),
                SWConfig(),
            ]
        ),

        
        
        # ================================================
        # FunctionType.EDIT
        # ================================================

        'noise': FunctionConfig(
            key = 'noise',
            name = 'Случайный шум',
            type = FunctionType.EDIT,
            function = noise,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=10, max=5000, step=10, default_value=600,
                    value_type=ValueType.INT, round_digits=0
                ),
                SLConfig(
                    name='R', title='Пороговое значение (R)',
                    min=0.1, max=1000, step=0.1, default_value=1,
                ),
                SLConfig(
                    name='delta', title='Шаг по оси X (delta)',
                    min=1, max=15, step=1, default_value=1,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        ),

        'my_noise': FunctionConfig(
            key = 'my_noise',
            name = 'Мой случайный шум',
            type = FunctionType.EDIT,
            function = my_noise,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=10, max=5000, step=10, default_value=600,
                    value_type=ValueType.INT, round_digits=0
                ),
                SLConfig(
                    name='R', title='Пороговое значение (R)',
                    min=0.1, max=1000, step=0.1, default_value=1,
                ),
                SLConfig(
                    name='delta', title='Шаг по оси X (delta)',
                    min=1, max=15, step=1, default_value=1,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        ),

        'shift': FunctionConfig(
            key = 'shift',
            name = 'Сдвиг',
            type = FunctionType.EDIT,
            function = shift,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='C', title='Значение смещения (C)',
                    min=-1000, max=1000, step=0.1, default_value=200,
                ),
                SLConfig(
                    name='N1', title='Cмещение от (N1)',
                    min=0, max=1000, step=1, default_value=100,
                    value_type=ValueType.INT, round_digits=0
                ),
                SLConfig(
                    name='N2', title='Cмещение до (N2)',
                    min=0, max=1000, step=1, default_value=500,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        ),

        'spikes': FunctionConfig(
            key = 'spikes',
            name = 'Одиночные выбросы',
            type = FunctionType.EDIT,
            function = spikes,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='N', title='Длина данных (N)',
                    min=10, max=10000, step=10, default_value=1000,
                    value_type=ValueType.INT, round_digits=0
                ),
                SLConfig(
                    name='M', title='Количество выбросов (M)',
                    min=1, max=100, step=1, default_value=10,
                    value_type=ValueType.INT, round_digits=0
                ),
                SLConfig(
                    name='R', title='Опорное значение (R)',
                    min=0.1, max=10000, step=0.1, default_value=10
                ),
                SLConfig(
                    name='Rs', title='Разброс (Rs)',
                    min=0.1, max=1000, step=0.1, default_value=5
                ),
                SWConfig(),
            ]
        ),

        'add_model': FunctionConfig(
            key = 'add_model',
            name = 'Поэлементное сложение',
            type = FunctionType.EDIT,
            function = add_model,
            parameters = [
                DDFDConfig(name='first_data', title='Выбор первого набора данных'),
                DDFDConfig(name='second_data', title='Выбор второго набора данных'),
                SWConfig(),
            ]
        ),

        'mult_model': FunctionConfig(
            key = 'mult_model',
            name = 'Поэлементное умножение',
            type = FunctionType.EDIT,
            function = mult_model,
            parameters = [
                DDFDConfig(name='first_data', title='Выбор первого набора данных'),
                DDFDConfig(name='second_data', title='Выбор второго набора данных'),
                SWConfig(),
            ]
        ),

        'anti_shift': FunctionConfig(
            key = 'anti_shift',
            name = 'Удаление смещения',
            type = FunctionType.EDIT,
            function = anti_shift,
            parameters = [
                DDFDConfig(),
                SWConfig(),
            ]
        ),

        'anti_spikes': FunctionConfig(
            key = 'anti_spikes',
            name = 'Удаление выбросов',
            type = FunctionType.EDIT,
            function = anti_spikes,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='R', title='Пороговое значение диапозона (R)',
                    min=0.1, max=1000, step=0.1, default_value=10,
                ),
                SWConfig(),
            ]
        ),

        'anti_trend_linear': FunctionConfig(
            key = 'anti_trend_linear',
            name = 'Удаление линейного тренда',
            type = FunctionType.EDIT,
            function = anti_trend_linear,
            parameters = [
                DDFDConfig(),
                SWConfig(),
            ]
        ),

        'anti_trend_non_linear': FunctionConfig(
            key = 'anti_trend_non_linear',
            name = 'Удаление НЕ линейного тренда',
            type = FunctionType.EDIT,
            function = anti_trend_non_linear,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='W', title='Длина скользящего окна (W)',
                    min=1, max=5000, step=1, default_value=10,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        ),

        'anti_noise': FunctionConfig(
            key = 'anti_noise',
            name = 'Удаление шума',
            type = FunctionType.EDIT,
            function = anti_noise,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='R', title='Пороговое значение шума (R)',
                ),
                TFDTConfig(
                    name='M', title='Кол-во осреднений (M)',
                    columns=[
                        TFDTColumn(
                            name='M', tooltip='Кол-во осреднений шума',
                            unit='шт', value_type=ValueType.INT
                        )
                    ],
                    default_value=[
                        TFDTItem(column_name='M', row_index=0, value=1),
                        TFDTItem(column_name='M', row_index=1, value=10),
                        TFDTItem(column_name='M', row_index=2, value=100),
                        TFDTItem(column_name='M', row_index=3, value=1000),
                        TFDTItem(column_name='M', row_index=4, value=10000),
                    ],
                ),
                SWConfig(),
            ]
        ),

        'convol_model': FunctionConfig(
            key = 'convol_model',
            name = 'Дискретная свёртка',
            type = FunctionType.EDIT,
            function = convol_model,
            parameters = [
                DDFDConfig(name='first_data', title='Выбор первого набора данных'),
                DDFDConfig(name='second_data', title='Выбор второго набора данных'),
                SLConfig(
                    name='M', title='Длина скользящего окна (M)',
                    min=1, max=1000, step=1, default_value=10,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        ),

        'scale_values': FunctionConfig(
            key = 'scale_values',
            name = 'Нормирование',
            type = FunctionType.EDIT,
            function = scale_values,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='new_min', title='Новое минимальное значение',
                    min=-1000, max=1000, step=0.001, default_value=-1,    
                ),
                SLConfig(
                    name='new_max', title='Новое максимальное значение',
                    min=-1000, max=1000, step=0.001, default_value=1,
                ),
                SWConfig(),
            ]
        ),

        'normalize_values': FunctionConfig(
            key = 'normalize_values',
            name = 'Нормализация',
            type = FunctionType.EDIT,
            function = normalize_values,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='new_max', title='Новое макс. значение (по модулю)',
                    min=0.0001, max=1000, step=0.001, default_value=1,
                ),
                SWConfig(),
            ]
        ),

        'absolute_value': FunctionConfig(
            key = 'absolute_value',
            name = 'Модуль',
            type = FunctionType.EDIT,
            function = absolute_value,
            parameters = [
                DDFDConfig(),
                SWConfig(),
            ]
        ),

        'extend_model': FunctionConfig(
            key = 'extend_model',
            name = 'Объединение данных',
            type = FunctionType.EDIT,
            function = extend_model,
            parameters = [
                DDFDConfig(name='first_data', title='Выбор первого набора данных'),
                DDFDConfig(name='second_data', title='Выбор второго набора данных'),
                SWConfig(),
            ]
        ),

        'lpf': FunctionConfig(
            key = 'lpf',
            name = 'Фильтр Низких Частот (ФНЧ)',
            type = FunctionType.EDIT,
            function = lpf,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='dt', title='Параметр (dt)',
                    min=0.0001, max=0.01, step=0.0001, default_value=0.002,
                    round_digits=4
                ),
                SLConfig(
                    name='Fc', title='Граничное значение (Fc)',
                    min=0.1, max=1000, step=0.01, default_value=50,    
                ),
                SLConfig(
                    name='m', title='Ширина окна (M)',
                    min=1, max=1000, step=1, default_value=64,
                    value_type=ValueType.INT, round_digits=0
                ),
            ]
        ),

        'hpf': FunctionConfig(
            key = 'hpf',
            name = 'Фильтра Высоких Частот (ФВЧ)',
            type = FunctionType.EDIT,
            function = hpf,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='dt', title='Параметр (dt)',
                    min=0.0001, max=0.01, step=0.0001, default_value=0.002,
                    round_digits=4 
                ),
                SLConfig(
                    name='Fc', title='Граничное значение (Fc)',
                    min=0.1, max=1000, step=0.01, default_value=50,    
                ),
                SLConfig(
                    name='m', title='Ширина окна (M)',
                    min=1, max=1000, step=1, default_value=64,
                    value_type=ValueType.INT, round_digits=0
                ),
            ]
        ),

        'bpf': FunctionConfig(
            key = 'bpf',
            name = 'Полосовой Фильтр (ПФ)',
            type = FunctionType.EDIT,
            function = bpf,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='dt', title='Параметр (dt)',
                    min=0.0001, max=0.01, step=0.0001, default_value=0.002,
                    round_digits=4
                ),
                SLConfig(
                    name='Fc1', title='Нижняя граница (Fc1)',
                    min=0.1, max=1000, step=0.01, default_value=35,    
                ),
                SLConfig(
                    name='Fc2', title='Верхняя граница (Fc2)',
                    min=0.1, max=1000, step=0.01, default_value=75,    
                ),
                SLConfig(
                    name='m', title='Ширина окна (M)',
                    min=1, max=1000, step=1, default_value=64,
                    value_type=ValueType.INT, round_digits=0
                ),
            ]
        ),

        'bsf': FunctionConfig(
            key = 'bsf',
            name = 'Режекторный Фильтр (РФ)',
            type = FunctionType.EDIT,
            function = bsf,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='dt', title='Параметр (dt)',
                    min=0.0001, max=0.01, step=0.0001, default_value=0.002,
                    round_digits=4
                ),
                SLConfig(
                    name='Fc1', title='Нижняя граница (Fc1)',
                    min=0.1, max=1000, step=0.01, default_value=35,
                ),
                SLConfig(
                    name='Fc2', title='Верхняя граница (Fc2)',
                    min=0.1, max=1000, step=0.01, default_value=75,    
                ),
                SLConfig(
                    name='m', title='Ширина окна (M)',
                    min=1, max=1000, step=1, default_value=64,
                    value_type=ValueType.INT, round_digits=0
                ),
            ]
        ),



        # ================================================
        # FunctionType.ANALYTIC
        # ================================================

        'statistics': FunctionConfig(
            key = 'statistics',
            name = 'Статистические данные',
            type = FunctionType.ANALYTIC,
            function = statistics,
            parameters = [
                DDFDConfig(),
            ],
            main_view = ViewType.TABLE_VERTICAL,
            view_list = [ViewType.TABLE_VERTICAL]
        ),

        'stationarity': FunctionConfig(
            key = 'stationarity',
            name = 'Стационарность',
            type = FunctionType.ANALYTIC,
            function = stationarity,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='M', title='Количество интервалов (M)',
                    min=2, max=100, step=1, default_value=10,
                    value_type=ValueType.INT, round_digits=0
                )
            ],
            main_view = ViewType.TABLE_VERTICAL,
            view_list = [ViewType.TABLE_VERTICAL]
        ),

        'hist': FunctionConfig(
            key = 'hist',
            name = 'Плотность вероятности',
            type = FunctionType.ANALYTIC,
            function = hist,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='M', title='Количество интервалов (M)',
                    min=1, max=100, step=1, default_value=10,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(name='is_density', title='Показывать плотность вероятности?'),
                SWConfig(),
            ],
            main_view = ViewType.HISTOGRAM,
            view_list = [ViewType.HISTOGRAM]
        ),

        'acf': FunctionConfig(
            key = 'acf',
            name = 'Автокорреляция',
            type = FunctionType.ANALYTIC,
            function = acf,
            parameters = [
                DDFDConfig(),
                DDConfig(
                    name='function_type', title='Тип коэффициента',
                    options=[
                        DDOptionItem(key='autocorrelation', text='Автокорреляция'),
                        DDOptionItem(key='covariance', text='Ковариация'),
                    ],
                    default_value='autocorrelation'
                ),
                SWConfig(),
            ]
        ),

        'ccf': FunctionConfig(
            key = 'ccf',
            name = 'Кросс-корреляция',
            type = FunctionType.ANALYTIC,
            function = ccf,
            parameters = [
                DDFDConfig(name='first_data', title='Выбор первого набора данных'),
                DDFDConfig(name='second_data', title='Выбор второго набора данных'),
                SWConfig(),
            ]
        ),

        'fourier': FunctionConfig(
            key = 'fourier',
            name = 'Прямое преобразование Фурье',
            type = FunctionType.ANALYTIC,
            function = fourier,
            parameters = [
                DDFDConfig(),
                SWConfig(),
                SWConfig(name='show_calculation_table', title='Показывать расчетную таблицу?'),
            ]
        ),

        'spectr_fourier': FunctionConfig(
            key = 'spectr_fourier',
            name = 'Амплитудный спектр Фурье',
            type = FunctionType.ANALYTIC,
            function = spectr_fourier,
            parameters = [
                DDFDConfig(),
                SLConfig(
                    name='delta_t', title='Шаг дисеретизации (delta_t)',
                    min=0.0001, max=0.01, step=0.0001, default_value=0.0005,
                    value_type=ValueType.FLOAT, round_digits=4
                ),
                SLConfig(
                    name='L_window', title='Длина окна (L_window)',
                    min=1, max=100, step=1, default_value=10,
                    value_type=ValueType.INT, round_digits=0
                ),
                SWConfig(),
            ]
        ),


    }
