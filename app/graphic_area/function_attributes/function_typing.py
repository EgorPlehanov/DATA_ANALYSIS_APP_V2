from typing import Optional, Callable, List
from collections import namedtuple
from dataclasses import dataclass
from pandas import DataFrame
from enum import Enum


class ParameterType(Enum):
    '''Тип параметра функции'''
    CHECKBOXES = 'checkboxes'
    DROPDOWN_FUNCTION_DATA = 'dropdown_function_data'
    DROPDOWN = 'dropdown'
    FILE_PICKER = 'file_picker'
    SLIDER = 'slider'
    SWITCH = 'switch'
    TEXTFIELDS_DATATABLE = 'textfields_datatable'
    TEXTFIELD = 'textfield'


class FunctionType(Enum):
    '''Тип функции'''
    DATA = 'data'
    EDIT = 'edit'
    ANALYTIC = 'analytic'


class ViewType(Enum):
    '''Тип представления результатов функции'''
    CHART = 'chart'
    HISTOGRAM = 'histogram'
    TABLE_HORIZONTAL = 'table_horizontal'
    TABLE_VERTICAL = 'table_vertical'


@dataclass
class ResultData:
    '''Результат выполнения функции
    
    main_data:              Основной набор данных
    type:                   Тип данных
    initial_data:           Начальные данные
    extra_data:             Дополнительные данные
    error_message:          Сообщение об ошибке
    view_chart:             Показывать график
    view_histogram:         Показывать гистограмму
    view_table_horizontal:  Показывать горизонтальную таблицу
    view_table_vertical:    Показывать вертикальную таблицу
    main_view:              Основное представление
    '''
    main_data: Optional[DataFrame]              = None
    type: Optional[str]                         = None
    initial_data: Optional[List['ResultData']]  = None
    extra_data: Optional[List['ResultData']]    = None
    error_message: Optional[str]                = None
    view_chart: Optional[bool]                  = None
    view_histogram: Optional[bool]              = None
    view_table_horizontal: Optional[bool]       = None
    view_table_vertical: Optional[bool]         = None
    main_view: Optional[ViewType]               = None


@dataclass
class FunctionConfig:
    '''Конфигурация функции'''
    key: str
    name: str
    type: FunctionType
    function: Callable
    parameters: dict

    def __post_init__(self):
        if not isinstance(self.key, str) or not self.key:
            raise ValueError(f'Недопустимый тип key: {type(self.key)}')
        if not isinstance(self.name, str) or not self.name:
            raise ValueError(f'Недопустимый тип name функции: {type(self.name)}')
        if not isinstance(self.type, FunctionType) or not self.type:
            raise ValueError(f'Недопустимый тип type: {self.type}, допустимые значения FunctionType')
        if not callable(self.function):
            raise ValueError(f'Недопустимый тип function: {type(self.function)}')
        if not isinstance(self.parameters, dict):
            raise ValueError(f'Недопустимый тип parameters функции: {type(self.parameters)}')


# Функция для меню выбора
FunctionOption = namedtuple('FunctionOption', ['key', 'name'])


class ValueType(Enum):
    '''Тип данных для валидации'''
    FUNCTION = 'function'
    INT = 'int'
    FLOAT = 'float'