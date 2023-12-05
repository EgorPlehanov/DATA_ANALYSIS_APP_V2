from .function_typing import ParameterType, ResultData, ViewType

from copy import deepcopy
from typing import Any
from inspect import signature


class FunctionCalculate:
    def __init__(self, function):
        self.function = function

        self.calculate_function = self.function.config.function

        self.parameters_config = self.function.config.parameters
        self.parameters_value = {}
        self.set_default_parameters_values()

        self.result = None
        self.calculate()


    def set_default_parameters_values(self) -> None:
        '''Устанавливает дефолтные значения параметров'''
        for param in self.parameters_config.values():
            self.parameters_value[param.name] = param.default_value
    

    def set_parameter_value(self, name: str, value: Any) -> None:
        '''Устанавливает значение параметра'''
        self.parameters_value[name] = value
        self.calculate()
        self.function.update_view()


    def get_current_parameter_value(self, name: str) -> Any:
        '''Возвращает значение параметра'''
        return deepcopy(self.parameters_value[name])


    def get_current_parameters(self) -> dict:
        '''Возвращает текущие значения параметров'''
        return deepcopy(self.parameters_value)
    

    def get_current_parameters_formatted(self) -> dict:
        '''Возвращает текущие значения параметров в виде строк'''
        formatted_parameters = {}
        for name, value in self.parameters_value.items():
            match self.parameters_config[name].type:
                case ParameterType.DROPDOWN_FUNCTION_DATA:
                    formatted_parameters[name] = value.formatted_name if value is not None else 'Не выбрано'
                case ParameterType.FILE_PICKER:
                    str_value = ', '.join([file.name for file in value]) if value is not None else 'Не выбрано'
                    formatted_parameters[name] = str_value
                case _:
                    formatted_parameters[name] = str(value)
        return formatted_parameters
    
    
    def calculate(self):
        '''Вычисляет значение функции'''
        try:
            valid_parameters = self._get_valid_parameters()
            function_result = self.calculate_function(**valid_parameters)

            initial_data = self._get_parameters_initial_data()
            view_list = self.function.config.view_list

            self.result = ResultData(
                main_data               = function_result.main_data,
                type                    = self._get_result_data_type(initial_data),
                initial_data            = initial_data,
                extra_data              = function_result.extra_data,
                error_message           = function_result.error_message,
                view_chart              = ViewType.CHART in view_list,
                view_histogram          = ViewType.HISTOGRAM in view_list,
                view_table_horizontal   = ViewType.TABLE_HORIZONTAL in view_list,
                view_table_vertical     = ViewType.TABLE_VERTICAL in view_list,
                main_view               = self.function.config.main_view
            )
        except Exception as e:
            self.result = ResultData(error_message = str(e))
        

    def _get_valid_parameters(self) -> dict:
        '''Возвращает текущие значения параметров функции с учетом сигнатуры функции'''
        function_parameters = signature(self.calculate_function).parameters

        valid_parameters = {
            name:
                self.parameters_value[name]
                if self.parameters_config[name].type != ParameterType.DROPDOWN_FUNCTION_DATA
                else self.parameters_value[name].get_result_main_data()
            for name in function_parameters if name in self.parameters_value
        }
        # TODO: добавить проверку типов с выбрасыванием исключения

        if len(valid_parameters) != len(function_parameters):
            raise ValueError("Количество параметров не совпадает")

        return valid_parameters


    def _get_parameters_initial_data(self) -> dict:
        '''Возвращает список результатов функций для параметров типа DROPDOWN_FUNCTION_DATA'''
        return [
            self.parameters_value[name].get_result()
            for name, param in self.parameters_config.items()
            if param.type == ParameterType.DROPDOWN_FUNCTION_DATA
        ]


    def _get_result_data_type(self, initial_data: list[ResultData]):
        '''Возвращает тип результата функции'''
        result_data_type = self.function.calculate_function_name
        initial_data_types = [data.type for data in initial_data]
        if len(initial_data_types) == 0:
            return result_data_type
        return result_data_type  + '(' + ', '.join(initial_data_types) + ')'
        
        