from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ParameterType

from dataclasses import dataclass
from flet import Container, Row, Text, Switch, LabelPosition, MainAxisAlignment


@dataclass
class SWConfig:
    name: str           = 'show_data_table'
    title: str          = 'Показывать таблицу данных?'
    default_value: bool = False

    @property
    def type(self) -> ParameterType:
        return ParameterType.SWITCH


class SwitchEditor(ParamEditorInterface, Container):
    def __init__(self, function, config: SWConfig = SWConfig()):
        self.function = function
        
        self._type = ParameterType.SWITCH
        self._name = config.name
        self.title = config.title
        self.default_value = config.default_value

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Row:
        return Row(
            controls = [
                Text(self.title),
                Switch(
                    label_position = LabelPosition.LEFT,
                    value = self.default_value,
                    on_change = self._on_change,
                )
            ],
            expand = True,
            alignment = MainAxisAlignment.SPACE_BETWEEN,
        )
    
    
    def _on_change(self, e) -> None:
        '''
        Обновляет значение параметра переключателя в экземпляре класса Function
        '''
        value = e.control.value
        self.function.calculate.set_parameter_value(self.name, value)

        self.update()
    