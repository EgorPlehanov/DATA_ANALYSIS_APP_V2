from ..function_typing import ParameterType
from .function_parameters import *

from flet import (
    Container, Column, Row, Markdown, border, colors
)


class FunctionParametersView(Container):
    def __init__(self, function):
        super().__init__()
        self.function = function

        self.parameters_config = self.function.config.parameters
        self.content = self.create_content()
        
        self.visible = False
        self.padding = 10
        self.width = 350


    def change_selection(self):
        '''Изменяет выделение (видимость) параметров'''
        self.visible = self.function.selected


    def create_content(self) -> Column:
        return Column(
            controls = [
                Markdown("### Параметры"),
                Column(
                    controls = self._create_parameters_list(),
                    tight = True
                )
            ],
            tight = True
        )
    

    def _create_parameters_list(self) -> list:
        '''Создает список предствалений параметров для отображения на экране'''
        parameters_list = []

        param_type_to_editor = {
            ParameterType.CHECKBOXES:             lambda function, config: CheckboxesEditor(function, config),
            ParameterType.DROPDOWN_FUNCTION_DATA: lambda function, config: DropdownFunctionDataEditor(function, config),
            ParameterType.DROPDOWN:               lambda function, config: DropdownEditor(function, config),
            ParameterType.FILE_PICKER:            lambda function, config: FilePickerEditor(function, config),
            ParameterType.SLIDER:                 lambda function, config: SliderEditor(function, config),
            ParameterType.SWITCH:                 lambda function, config: SwitchEditor(function, config),
            ParameterType.TEXTFIELDS_DATATABLE:   lambda function, config: TextFieldsDataTableEditor(function, config),
            ParameterType.TEXTFIELD:              lambda function, config: TextFieldEditor(function, config),
        }

        for config in self.parameters_config.values():
            param_type = config.type
            param_editor = param_type_to_editor[param_type](self.function, config)
                    
            parameters_list.append(
                Container(
                    content = param_editor,
                    data = param_type,
                    padding = 10,
                    border_radius = 10,
                    border = border.all(1, colors.with_opacity(0.05, colors.SECONDARY)),
                    bgcolor = colors.BLACK12,
                )
            )
        return parameters_list
