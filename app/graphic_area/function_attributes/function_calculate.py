from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..function import Function

from .function_typing import ParameterType, ResultData, ViewType, FunctionResult

from typing import Any, get_type_hints
from inspect import signature
from collections import defaultdict


class FunctionCalculate:
    def __init__(self, function: "Function"):
        self.function = function

        self.calculate_function = self.function.config.function
        self.calculate_function_type_hints = self.get_signature_type_hints()

        self.parameters_configs = self.function.config.parameters
        self.parameters_value = {}
        self.set_default_parameters_values()

        self.result = None
        self.calculate()


    def get_signature_type_hints(self):
        '''Возвращает типы параметров функции'''
        type_hints = get_type_hints(self.calculate_function)
        type_hints.pop('return', None)
        return {
            name: type_hints.get(name)
            for name in signature(self.calculate_function).parameters
        }


    def set_default_parameters_values(self) -> None:
        '''Устанавливает дефолтные значения параметров'''
        for config in self.parameters_configs.values():
            match config.type:
                case ParameterType.TEXTFIELDS_DATATABLE:
                    self.parameters_value[config.name] = self._get_default_values_textfields_datatable(config)
                case _:
                    self.parameters_value[config.name] = config.default_value


    def _get_default_values_textfields_datatable(self, config) -> dict:
        '''Возвращает значение по умолчанию для параметра с типом TEXTFIELDS_DATATABLE'''
        rows = defaultdict(list)
        for cell in config.default_value:
            rows[cell.row_index].append(cell)
        return {
            row_idx: {
                cell.column_name: cell.value
                for cell in cells
            }
            for row_idx, cells in rows.items()
            if all(cell.value != '' for cell in cells)
        }
    

    def set_parameter_value(self, name: str, value: Any) -> None:
        '''Устанавливает значение параметра'''
        self.parameters_value[name] = value
        self.calculate()
        self.function.update_view()


    def get_current_parameter_value(self, name: str) -> Any:
        '''Возвращает значение параметра'''
        return self.parameters_value[name]


    def get_current_parameters(self) -> dict:
        '''Возвращает текущие значения параметров'''
        return self.parameters_value
    

    def get_current_parameters_formatted(self) -> dict:
        '''Возвращает текущие значения параметров в виде строк'''
        empty_value = 'Не задано'
        formatted_parameters = {}

        for name, value in self.parameters_value.items():
            match self.parameters_configs[name].type:
                case ParameterType.DROPDOWN_FUNCTION_DATA:
                    str_value = value.formatted_name if value is not None else empty_value
                case ParameterType.FILE_PICKER:
                    str_value = ', '.join([file.name for file in value]) if value is not None and len(value) else empty_value
                case ParameterType.TEXTFIELDS_DATATABLE:
                    str_value = str(value).replace('**', '\*\*') if value else empty_value
                case ParameterType.DATA_LIBRARY:
                    str_value = value.name if value is not None else empty_value
                case ParameterType.CHECKBOXES:
                    str_value = f"[{', '.join([str(key) for key in value])}]" if len(value) else empty_value
                case ParameterType.TEXTFIELD:
                    str_value = value if value != '' else empty_value
                case _:
                    str_value = str(value)
            formatted_parameters[name] = str_value
        return formatted_parameters
    
    
    def calculate(self):
        '''Вычисляет значение функции'''
        try:
            valid_parameters = self._get_valid_parameters()
            function_result: FunctionResult = self.calculate_function(**valid_parameters)
            if not isinstance(function_result, FunctionResult):
                raise Exception(f"Результат функции должен быть типа FunctionResult, а не {type(function_result)}")

            self._set_function_color_to_extra_data(function_result)
            initial_data = self._get_parameters_initial_data()
            view_list = self._get_view_list()

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
                main_view               = self.function.config.main_view,
                color                   = self.function.color
            )
        except Exception as e:
            self.result = ResultData(error_message = str(e))
        

    def _get_valid_parameters(self) -> dict:
        '''Возвращает текущие значения параметров функции с учетом сигнатуры функции'''
        valid_parameters = {
            name:
                self.parameters_value[name].get_result_main_data()
                if (
                    self.parameters_configs[name].type == ParameterType.DROPDOWN_FUNCTION_DATA
                    and self.parameters_value[name] is not None
                )
                else self.parameters_value[name]
            for name in self.calculate_function_type_hints
            if self.is_valid_parameter(name)
        }

        if len(valid_parameters) != len(self.calculate_function_type_hints):
            raise ValueError(
                "Количество параметров не совпадает, "
                + f"ожидалось {len(self.calculate_function_type_hints)} и получено {len(valid_parameters)}\n"
                + f"\nПараметры: {self.calculate_function_type_hints}"
                + f"\nВалидные: {valid_parameters}"
            )

        return valid_parameters
    

    def is_valid_parameter(self, name: str) -> bool:
        '''Возвращает True, если параметр имеет допустимый тип'''
        if name not in self.parameters_value:
            return False
        if (
            (
                self.calculate_function_type_hints[name] in [bool, int, str]
                and not type(self.parameters_value[name]) == self.calculate_function_type_hints[name]
            ) or (
                self.calculate_function_type_hints[name] in [float]
                and not isinstance(self.parameters_value[name], (float, int))
            )
        ):
            raise TypeError(f"Тип параметра {name} должен быть типа {self.calculate_function_type_hints[name]}, а не {type(self.parameters_value[name])}")
        return True


    def _get_parameters_initial_data(self) -> list[ResultData]:
        '''Возвращает список результатов функций для параметров типа DROPDOWN_FUNCTION_DATA'''
        return [
            self.parameters_value[name].get_result()
            for name, param in self.parameters_configs.items()
            if (
                param.type == ParameterType.DROPDOWN_FUNCTION_DATA
                and self.parameters_value[name] is not None
                and self.parameters_value[name].get_result().main_data is not None
            )
        ]
    

    def _get_view_list(self) -> list[ViewType]:
        '''Возвращает список типов отображения'''
        view_list = []
        view_list.extend(self.function.config.view_list)
        if (
            'show_data_table' in self.parameters_configs
            and self.parameters_configs['show_data_table'].type == ParameterType.SWITCH
            and self.parameters_value['show_data_table']
        ):
            view_list.append(ViewType.TABLE_HORIZONTAL)

        return view_list
    

    def _set_function_color_to_extra_data(self, function_result: FunctionResult) -> None:
        '''Устанавливает цвет функции в дополнительных данных'''
        if function_result.extra_data is not None:
            for data in function_result.extra_data:
                data.color = self.function.color


    def _get_result_data_type(self, initial_data: list[ResultData]) -> str:
        '''Возвращает тип результата функции'''
        result_data_type = self.function.calculate_function_name
        initial_data_types = [data.type for data in initial_data]
        if len(initial_data_types) == 0:
            return result_data_type
        return result_data_type  + '(' + ', '.join(initial_data_types) + ')'
        