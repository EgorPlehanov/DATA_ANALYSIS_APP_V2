from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...function import Function

from ..function_typing import ParameterType
from .function_parameters import *

from flet import (
    Container, Column, Markdown, padding
)


class FunctionParametersView(Container):
    '''Представление параметров функции'''
    def __init__(self, function: "Function"):
        super().__init__()
        self.function = function

        self.parameters_config = self.function.config.parameters
        self.list_parameters = self._create_parameters_list()
        self.content = self.create_content()
        
        self.visible = False
        self.padding = padding.only(right=10, top=10, bottom=10)
        self.width = 350


    def change_selection(self):
        '''Изменяет выделение (видимость) параметров'''
        self.visible = self.function.selected


    def create_content(self) -> Column:
        return Column(
            controls = [
                Markdown("### Параметры"),
                Column(
                    controls = self.list_parameters,
                    tight = True
                )
            ],
            tight = True
        )
    

    def _create_parameters_list(self) -> list:
        '''Создает список предствалений параметров для отображения на экране'''
        parameters_list = []

        param_type_to_editor = {
            ParameterType.CHECKBOXES:             CheckboxesEditor,
            ParameterType.DROPDOWN_FUNCTION_DATA: DropdownFunctionDataEditor,
            ParameterType.DROPDOWN:               DropdownEditor,
            ParameterType.FILE_PICKER:            FilePickerEditor,
            ParameterType.SLIDER:                 SliderEditor,
            ParameterType.SWITCH:                 SwitchEditor,
            ParameterType.TEXTFIELDS_DATATABLE:   TextFieldsDataTableEditor,
            ParameterType.TEXTFIELD:              TextFieldEditor,
            ParameterType.DATA_LIBRARY:           DataLibraryEditor,
            ParameterType.RANGE_SLIDER:           RangeSliderEditor
        }

        for config in self.parameters_config.values():
            parameters_list.append(
                param_type_to_editor[config.type](self.function, config)
            )
        return parameters_list
    

    def update_dependencies_parameters(self):
        '''Вызывает методы для обновления параметров зависимых функций'''
        for param in self.list_parameters:
            if param.type == ParameterType.DROPDOWN_FUNCTION_DATA:
                param.update_values()
        
