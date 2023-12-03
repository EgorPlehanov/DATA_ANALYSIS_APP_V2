from .function_typing import ParameterType, ResultData

from copy import deepcopy
from typing import Any
from inspect import signature


class FunctionCalculate:
    def __init__(self, function):
        self.function = function

        self.calculate_function = self.function.config.function

        self.parameters_config = self.function.config.parameters
        self.parameters_value = {}
        self.set_default_parameters()

        self.result = None
        self.calculate()


    def set_default_parameters(self) -> None:
        '''Устанавливает дефолтные значения параметров'''
        for param in self.parameters_config.values():
            self.parameters_value[param.name] = param.default_value


    def get_current_parameters(self) -> dict:
        '''Возвращает текущие значения параметров'''
        return deepcopy(self.parameters_value)
    

    def get_current_parameters_formatted(self) -> dict:
        '''Возвращает текущие значения параметров в виде строк'''
        parameters = {}
        for name, value in self.parameters_value.items():
            match self.parameters_config[name].type:
                case ParameterType.DROPDOWN_FUNCTION_DATA:
                    parameters[name] = value.formatted_name
                case _:
                    parameters[name] = str(value)
        return parameters
    

    def set_parameter_value(self, name: str, value: Any) -> None:
        '''Устанавливает значение параметра'''
        self.parameters_value[name] = value
    
    
    def calculate(self):
        '''Вычисляет значение функции'''
        function_parameters = signature(self.calculate_function).parameters
        valid_parameters = {
            name: self.parameters_value[name]
            for name in function_parameters
            if (
                name in self.parameters_value
                and name not in ['show_table_data']
            )
        }
        if len(valid_parameters) != len(function_parameters):
            raise ValueError("Количество параметров не совпадает")
        
        main_data = self.calculate_function(**valid_parameters)

        self.result = ResultData(
            main_data = main_data,
            type = self.function.calculate_function_name,
            initial_data=None,
            extra_data=None,
            error_message=None,
            view_chart=None,
            view_histogram=None,
            view_table_horizontal=None,
            view_table_vertical=None,
            main_view=None
        )



