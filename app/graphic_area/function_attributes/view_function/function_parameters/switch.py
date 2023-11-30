from .parameter_editor_interface import ParamEditorInterface

from dataclasses import dataclass
from flet import Container, Row, Text, Switch, LabelPosition, MainAxisAlignment


@dataclass
class SWConfig:
    name: str           = 'show_data_table'
    title: str          = 'Показывать таблицу данных?'
    default_value: bool = False


class SwitchEditor(ParamEditorInterface, Container):
    def __init__(self, config: SWConfig = SWConfig()):
        self._type = 'switch'
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
        switch_value = e.control.value
        # self.function.set_parameter_value(self._param_name, switch_value)

        # self.update_function_card()
    