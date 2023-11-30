from .param_editor_interface import ParamEditorInterface

from flet import Container, Row, Text, Switch, LabelPosition, MainAxisAlignment


class SwitchEditor(ParamEditorInterface, Container):
    def __init__(self,
        name: str           = 'show_data_table',
        title: str          = 'Показывать таблицу данных?',
        default_value: bool = False
    ):
        self._type = 'switch'
        self._name = name
        self.title = title
        self.default_value = default_value

        super().__init__()
        self.set_styles()
        self.content = self.create_content()


    def create_content(self) -> Row:
        return Row(
            controls = [
                Text(self.title),
                Switch(
                    label_position = LabelPosition.LEFT,
                    value = self.default_value,
                    on_change = self.on_change,
                )
            ],
            expand = True,
            alignment = MainAxisAlignment.SPACE_BETWEEN,
        )
    
    
    def on_change(self, e) -> None:
        '''
        Обновляет значение параметра переключателя в экземпляре класса Function
        '''
        switch_value = e.control.value
        # self.function.set_parameter_value(self._param_name, switch_value)

        # self.update_function_card()
    