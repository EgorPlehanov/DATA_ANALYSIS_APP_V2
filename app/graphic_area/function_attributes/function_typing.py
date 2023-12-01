from typing import Optional, Callable, List
from collections import namedtuple
from dataclasses import dataclass
from pandas import DataFrame
from enum import Enum


@dataclass
class ResultData:
    main_data: Optional[DataFrame]              = None
    type: Optional[str]                         = None
    initial_data: Optional[List['ResultData']]  = None
    extra_data: Optional[List['ResultData']]    = None
    error_message: Optional[str]                = None
    view_chart: Optional[bool]                  = None
    view_histogram: Optional[bool]              = None
    view_table_horizontal: Optional[bool]       = None
    view_table_vertical: Optional[bool]         = None
    main_view: Optional[str]                    = None


class FunctionType(Enum):
    DATA = 'data'
    EDIT = 'edit'
    ANALYTIC = 'analytic'


@dataclass
class FunctionConfig:
    key: str
    name: str
    type: FunctionType
    function: Callable
    parameters: list

    def __post_init__(self):
        if not isinstance(self.key, str) or not self.key:
            raise ValueError(f'Недопустимый тип key: {type(self.key)}')
        if not isinstance(self.name, str) or not self.name:
            raise ValueError(f'Недопустимый тип name функции: {type(self.name)}')
        if not isinstance(self.type, FunctionType) or not self.type:
            raise ValueError(f'Недопустимый тип type: {self.type}, допустимые значения FunctionType')
        if not callable(self.function):
            raise ValueError(f'Недопустимый тип function: {type(self.function)}')
        if not isinstance(self.parameters, list):
            raise ValueError(f'Недопустимый тип parameters функции: {type(self.parameters)}')


FunctionOption = namedtuple('FunctionOption', ['key', 'name'])


class ValueType(Enum):
    FUNCTION = 0
    INT = 1
    FLOAT = 2