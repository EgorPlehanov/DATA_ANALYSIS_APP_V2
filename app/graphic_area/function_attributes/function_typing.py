from typing import Optional, Callable, List, Dict
from dataclasses import dataclass, field
from pandas import DataFrame
from enum import Enum
from random import choice
from flet import colors
import os



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
    DATA_LIBRARY = 'data_library'
    RANGE_SLIDER = 'range_slider'

    def __str__(self):
        return self.value



class FunctionType(Enum):
    '''Тип функции'''
    TEST = 'test'
    DATA = 'data'
    EDIT = 'edit'
    ANALYTIC = 'analytic'

    def __str__(self):
        return self.value



class ViewType(Enum):
    '''Тип представления результатов функции'''
    CHART = 'chart'
    HISTOGRAM = 'histogram'
    TABLE_HORIZONTAL = 'table_horizontal'
    TABLE_VERTICAL = 'table_vertical'
    AUDIO_PLAYER = 'audio_player'

    def __str__(self):
        return self.value



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
    view_chart: Optional[bool]                  = True
    view_histogram: Optional[bool]              = None
    view_table_horizontal: Optional[bool]       = None
    view_table_vertical: Optional[bool]         = None
    view_audio: Optional[bool]                  = None
    main_view: Optional[ViewType]               = ViewType.CHART
    color: Optional[str]                        = colors.BLACK



@dataclass
class FunctionResult:
    '''Результат выполнения функции (значение которое должна возвращать каждая функция для calculate)
    
    main_data:  Основной набор данных
    extra_data: Дополнительные данные
    error_message: Сообщение об ошибке
    '''
    main_data: Optional[DataFrame]          = None
    extra_data: Optional[List[ResultData]]  = None
    error_message: Optional[str]            = None

    def __post_init__(self):
        '''Округляет и удаляет значения больше заданного порога в датафрейме'''
        max_value: int = 1000000000
        decimal_places: int = 4
        def round_and_clip(value):
            try:
                numeric_value = value
                if isinstance(numeric_value, (str)):
                    numeric_value = float(value.replace(',', '.'))
                return round(numeric_value, decimal_places) if numeric_value <= max_value else max_value
            except ValueError:
                return value
            
        if self.main_data is not None and isinstance(self.main_data, DataFrame):
            self.main_data = self.main_data.map(round_and_clip)

        if self.extra_data is not None:
            if not isinstance(self.extra_data, list):
                self.extra_data = [self.extra_data]
            for data in self.extra_data:
                if data.main_data is not None and isinstance(data.main_data, DataFrame):
                    data.main_data = data.main_data.map(round_and_clip)



@dataclass
class FunctionConfig:
    '''Конфигурация функции
    
    key - ключ функции
    name - название функции
    type - тип функции
    enabled - активна ли функция
    function - функция
    parameters - параметры функции
    main_view - основное представление функции
    view_list - список представлений функции
    '''
    key: str                  = 'Unknown'
    name: str                 = 'Неизвестная'
    type: FunctionType        = FunctionType.DATA
    enabled: bool             = True
    function: Callable        = lambda: None
    parameters: Dict | List   = field(default_factory=dict)
    main_view: ViewType       = ViewType.CHART
    view_list: List[ViewType] = field(default_factory=lambda: [ViewType.CHART])

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
            if isinstance(self.parameters, list):
                self.parameters = {param.name: param for param in self.parameters}
            else:
                raise ValueError(f'Недопустимый тип parameters функции: {type(self.parameters)}')
        if not isinstance(self.main_view, ViewType) or not self.main_view:
            raise ValueError(f'Недопустимый тип main_view функции: {type(self.main_view)}, допустимые значения ViewType')
        if (
            not isinstance(self.view_list, list)
            or not all(isinstance(view, ViewType) for view in self.view_list)
        ):
            raise ValueError(f'Недопустимый тип view_list функции: {type(self.view_list)}, допустимые значения ViewType')



# Функция для меню выбора
@dataclass
class FunctionMenuOption:
    '''Опция меню выбора функции'''
    key: str
    name: str



class ValueType(Enum):
    '''Тип данных для валидации'''
    FUNCTION = 'function'
    INT = 'int'
    FLOAT = 'float'

    def __str__(self):
        return self.value



class Color(Enum):
    '''Цвет'''
    RED         = "#ff0000"
    PINK        = "#ff0072"
    PURPLE      = "#AA00FF"
    DEEP_PURPLE = "#6a00ff"
    INDIGO      = "#0026ff"
    BLUE        = "#2962FF"
    LIGHT_BLUE  = "#0091EA"
    CYAN        = "#00ddff"
    TEAL        = "#00ffdc"
    GREEN       = "#00ff69"
    LIGHT_GREEN = "#63ff00"
    LIME        = "#bdff00"
    YELLOW      = "#FFD600"
    AMBER       = "#FFAB00"
    ORANGE      = "#FF6D00"
    DEEP_ORANGE = "#DD2C00"

    def __str__(self):
        return str(self.value)
    
    @classmethod
    def random(cls):
        '''Возвращает случайное значение цвета'''
        return choice(list(cls))



@dataclass
class File:
    '''Файл
    
    path - путь к файлу
    name - имя файла
    extension - расширение файла
    size - размер файла (байт)
    size_formatted - размер файла в строку
    formatted_name - имя файла и его размер
    data_path - путь к файлу внутри папки "DATA"
    folder - имя папки, в которой находится файл
    '''
    path: str = None

    def __post_init__(self):
        self.name = os.path.basename(self.path)
        self.extension = self.path.split('.')[-1].lower()
        self.size = os.path.getsize(self.path)
        self.size_formatted = self.convert_size(self.size)
        self.formatted_name = f"{self.name} ({self.size_formatted})"
        self.data_path = self.path.replace("DATA\\", "").replace("\\", " > ")
        self.folder = os.path.basename(os.path.dirname(self.path))
    
    def convert_size(self, size) -> str:
        '''Конвертирует размер файла в байтах в строку'''
        if not size:
            return "0\u00A0байт"
        elif size < 1024:
            return f"{size}\u00A0байт"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f}\u00A0КБ"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.2f}\u00A0МБ"
        else:
            return f"{size / (1024 * 1024 * 1024):.2f}\u00A0ГБ"



@dataclass
class Range:
    start_value: int | float = 0
    end_value: int | float   = 1

    def __post_init__(self):
        if self.start_value > self.end_value:
            self.start_value, self.end_value = self.end_value, self.start_value

    def __str__(self):
        return f"(start_value: {self.start_value}, end_value: {self.end_value})"